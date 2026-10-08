import unittest

from django.conf import settings
from django.test import TestCase

from api.models import Post, PostLike
from api.services import PostService, UserService
from api.tests.helpers import auth_client, make_post, make_user

PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


class CreatePostApiTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.client = auth_client(self.alice)

    def test_create_post_stores_it_for_the_authenticated_user(self):
        response = self.client.post("/api/post/", {"post": "hello world"}, format="json")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["post"]["post"], "hello world")
        self.assertEqual(data["post"]["user"]["username"], "alice")
        self.assertEqual(Post.objects.get().user, self.alice)

    def test_create_post_over_the_length_limit_is_rejected(self):
        response = self.client.post("/api/post/", {"post": "x" * 256}, format="json")

        self.assertIn("post", response.json()["errors"])
        self.assertEqual(Post.objects.count(), 0)

    # Known bug: a body without a "post" field raises KeyError in
    # PostSerializer.save and the server answers 500 instead of 400. Remove
    # the decorator when fixed.
    @unittest.expectedFailure
    def test_create_post_without_content_is_a_client_error(self):
        response = self.client.post("/api/post/", {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Post.objects.count(), 0)


class EditPostApiTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.post = make_post(self.alice, "before")

    def test_get_post_returns_it(self):
        response = auth_client(self.bob).get(f"/api/post/{self.post.id}")

        self.assertEqual(response.json()["post"], "before")

    def test_get_unknown_post_returns_an_error_body(self):
        response = auth_client(self.bob).get("/api/post/999")

        self.assertEqual(response.json()["errors"]["messages"], ["Post not found"])


class LikeApiTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.post = make_post(self.alice)
        self.client = auth_client(self.bob)

    def test_like_returns_updated_counts(self):
        response = self.client.put(
            f"/api/post/{self.post.id}/like/", {"is_like": True}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["like_count"], 1)
        self.assertEqual(data["dislike_count"], 0)

    def test_dislike_after_like_switches_the_reaction(self):
        url = f"/api/post/{self.post.id}/like/"
        self.client.put(url, {"is_like": True}, format="json")

        data = self.client.put(url, {"is_like": False}, format="json").json()

        self.assertEqual(data["like_count"], 0)
        self.assertEqual(data["dislike_count"], 1)
        self.assertEqual(PostLike.objects.filter(post=self.post).count(), 1)

    def test_unlike_removes_the_reaction(self):
        self.client.put(f"/api/post/{self.post.id}/like/", {"is_like": True}, format="json")

        response = self.client.put(
            f"/api/post/{self.post.id}/unlike/", {"unlike": True}, format="json"
        )

        self.assertTrue(response.json()["success"])
        self.assertEqual(PostLike.objects.count(), 0)

    # Known bug: PostLikeView and PostUnLikeView return None when the
    # serializer is invalid, so DRF raises an AssertionError and the server
    # answers 500 instead of 400. Remove the decorators when fixed.
    @unittest.expectedFailure
    def test_like_without_is_like_is_a_client_error(self):
        response = self.client.put(f"/api/post/{self.post.id}/like/", {}, format="json")

        self.assertEqual(response.status_code, 400)

    @unittest.expectedFailure
    def test_unlike_without_unlike_flag_is_a_client_error(self):
        response = self.client.put(f"/api/post/{self.post.id}/unlike/", {}, format="json")

        self.assertEqual(response.status_code, 400)


class FollowApiTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.client = auth_client(self.bob)

    def test_follow_returns_both_users_details(self):
        response = self.client.put("/api/alice/follow/", {"follow": True}, format="json")

        data = response.json()
        self.assertEqual(data["follower"]["username"], "bob")
        self.assertEqual(data["follower"]["followees"], ["alice"])
        self.assertEqual(data["followee"]["username"], "alice")
        self.assertEqual(data["followee"]["followers"], ["bob"])

    def test_unfollow_clears_the_relationship(self):
        self.client.put("/api/alice/follow/", {"follow": True}, format="json")

        data = self.client.put("/api/alice/follow/", {"follow": False}, format="json").json()

        self.assertEqual(data["follower"]["followees"], [])
        self.assertEqual(data["followee"]["followers"], [])

    def test_follow_unknown_user_returns_an_error_body(self):
        response = self.client.put("/api/nobody/follow/", {"follow": True}, format="json")

        self.assertIn("nobody", response.json()["errors"]["messages"][0])

    def test_follow_requires_the_follow_flag(self):
        response = self.client.put("/api/alice/follow/", {}, format="json")

        self.assertIn("follow", response.json()["errors"])

    def test_profile_shows_followers_and_followees(self):
        UserService.follow_user(self.bob, "alice", True)

        data = self.client.get("/api/alice/profile/").json()

        self.assertEqual(data["username"], "alice")
        self.assertEqual(data["followers"], ["bob"])
        self.assertEqual(data["followees"], [])

    def test_profile_of_unknown_user_returns_an_error_body(self):
        data = self.client.get("/api/nobody/profile/").json()

        self.assertIn("nobody", data["errors"]["messages"][0])


class FeedApiTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.carol = make_user("carol")
        self.client = auth_client(self.bob)

    def _ids(self, response):
        return [post["id"] for post in response.json()["results"]]

    def test_all_posts_feed_includes_everyones_posts_newest_first(self):
        old = make_post(self.alice, "old", age_minutes=30)
        new = make_post(self.carol, "new", age_minutes=1)

        response = self.client.get("/api/posts/")

        self.assertEqual(self._ids(response), [new.id, old.id])

    def test_all_posts_feed_is_paginated_without_gaps_or_duplicates(self):
        total = PAGE_SIZE + 3
        posts = [make_post(self.alice, f"post {i}", age_minutes=i) for i in range(total)]
        expected = [post.id for post in posts]  # age_minutes ascending == newest first

        first = self.client.get("/api/posts/").json()
        self.assertEqual(first["count"], total)
        self.assertEqual(len(first["results"]), PAGE_SIZE)
        self.assertIsNone(first["previous"])
        self.assertIsNotNone(first["next"])

        second = self.client.get(first["next"]).json()
        self.assertEqual(len(second["results"]), 3)
        self.assertIsNone(second["next"])

        ids = [p["id"] for p in first["results"]] + [p["id"] for p in second["results"]]
        self.assertEqual(ids, expected)

    def test_feed_marks_the_callers_reaction_and_counts(self):
        liked = make_post(self.alice, "liked", age_minutes=3)
        disliked = make_post(self.alice, "disliked", age_minutes=2)
        untouched = make_post(self.alice, "untouched", age_minutes=1)
        PostService.update_post_like(self.bob, liked.id, True)
        PostService.update_post_like(self.carol, liked.id, True)
        PostService.update_post_like(self.bob, disliked.id, False)

        results = {p["id"]: p for p in self.client.get("/api/posts/").json()["results"]}

        self.assertTrue(results[liked.id]["is_liked"])
        self.assertFalse(results[liked.id]["is_disliked"])
        self.assertEqual(results[liked.id]["like_count"], 2)
        self.assertTrue(results[disliked.id]["is_disliked"])
        self.assertEqual(results[disliked.id]["dislike_count"], 1)
        self.assertFalse(results[untouched.id]["is_liked"])
        self.assertFalse(results[untouched.id]["is_disliked"])

    def test_reactions_belong_to_the_requesting_user(self):
        post = make_post(self.alice)
        PostService.update_post_like(self.carol, post.id, True)

        result = self.client.get("/api/posts/").json()["results"][0]

        self.assertFalse(result["is_liked"])
        self.assertEqual(result["like_count"], 1)

    def test_following_feed_only_contains_followed_users(self):
        UserService.follow_user(self.bob, "alice", True)
        wanted = make_post(self.alice, "from alice")
        make_post(self.carol, "from carol")
        make_post(self.bob, "from bob")

        response = self.client.get("/api/posts/following/")

        self.assertEqual(self._ids(response), [wanted.id])

    def test_following_feed_is_empty_when_following_nobody(self):
        make_post(self.alice)

        data = self.client.get("/api/posts/following/").json()

        self.assertEqual(data["count"], 0)
        self.assertEqual(data["results"], [])

    def test_user_feed_only_contains_that_users_posts(self):
        mine = make_post(self.alice, "alice's")
        make_post(self.carol, "carol's")

        response = self.client.get("/api/alice/posts/")

        self.assertEqual(self._ids(response), [mine.id])

    def test_user_feed_for_unknown_user_returns_an_error_body(self):
        data = self.client.get("/api/nobody/posts/").json()

        self.assertIn("nobody", data["errors"]["messages"][0])
