import unittest

from django.test import TestCase

from api.models import Chat, ChatMessage, Post, PostLike
from api.services import ChatService, PostService, UserService
from api.tests.helpers import make_post, make_user


class UserServiceTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")

    def test_get_profile_returns_the_user(self):
        result = UserService.get_profile("alice")

        self.assertTrue(result["success"])
        self.assertEqual(result["user"], self.alice)

    def test_get_profile_of_unknown_user_fails(self):
        result = UserService.get_profile("nobody")

        self.assertFalse(result["success"])
        self.assertIn("nobody", result["message"])

    def test_follow_links_both_sides(self):
        result = UserService.follow_user(self.bob, "alice", True)

        self.assertTrue(result["success"])
        self.assertEqual(result["user"], self.alice)
        self.assertIn(self.bob, self.alice.followers.all())
        self.assertIn(self.alice, self.bob.followees.all())

    def test_follow_is_one_directional(self):
        UserService.follow_user(self.bob, "alice", True)

        self.assertNotIn(self.alice, self.bob.followers.all())
        self.assertNotIn(self.bob, self.alice.followees.all())

    def test_following_twice_does_not_duplicate(self):
        UserService.follow_user(self.bob, "alice", True)
        UserService.follow_user(self.bob, "alice", True)

        self.assertEqual(self.alice.followers.count(), 1)

    def test_unfollow_removes_the_link(self):
        UserService.follow_user(self.bob, "alice", True)

        result = UserService.follow_user(self.bob, "alice", False)

        self.assertTrue(result["success"])
        self.assertEqual(self.alice.followers.count(), 0)
        self.assertEqual(self.bob.followees.count(), 0)

    def test_unfollow_without_following_is_harmless(self):
        result = UserService.follow_user(self.bob, "alice", False)

        self.assertTrue(result["success"])
        self.assertEqual(self.alice.followers.count(), 0)

    def test_follow_unknown_user_fails(self):
        result = UserService.follow_user(self.bob, "nobody", True)

        self.assertFalse(result["success"])
        self.assertIn("nobody", result["message"])

    # Known bug: nothing stops a user following themselves, so they end up in
    # their own followers and followees. Remove the decorator when fixed.
    @unittest.expectedFailure
    def test_cannot_follow_yourself(self):
        result = UserService.follow_user(self.bob, "bob", True)

        self.assertFalse(result["success"])
        self.assertEqual(self.bob.followers.count(), 0)


class PostServiceTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")

    def test_create_post(self):
        post, created = PostService.create_post(user=self.alice, post="hello")

        self.assertTrue(created)
        self.assertEqual(post.user, self.alice)
        self.assertEqual(Post.objects.get(pk=post.pk).post, "hello")

    def test_get_post_returns_none_for_unknown_id(self):
        self.assertIsNone(PostService.get_post(999))

    def test_owner_can_edit_a_post(self):
        post = make_post(self.alice, "before")

        result = PostService.edit_post(self.alice, post.id, "after")

        self.assertTrue(result["success"])
        post.refresh_from_db()
        self.assertEqual(post.post, "after")

    def test_other_user_cannot_edit_a_post(self):
        post = make_post(self.alice, "before")

        result = PostService.edit_post(self.bob, post.id, "hijacked")

        self.assertFalse(result["success"])
        post.refresh_from_db()
        self.assertEqual(post.post, "before")

    def test_edit_unknown_post_fails(self):
        result = PostService.edit_post(self.alice, 999, "x")

        self.assertFalse(result["success"])


class PostLikeServiceTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.post = make_post(self.alice)

    def test_like_adds_a_like(self):
        result = PostService.update_post_like(self.bob, self.post.id, True)

        self.assertTrue(result["success"])
        self.assertEqual(result["like_count"], 1)
        self.assertEqual(result["dislike_count"], 0)
        self.assertIs(PostService.is_post_liked(self.post.id, self.bob), True)

    def test_dislike_adds_a_dislike(self):
        result = PostService.update_post_like(self.bob, self.post.id, False)

        self.assertEqual(result["like_count"], 0)
        self.assertEqual(result["dislike_count"], 1)
        self.assertIs(PostService.is_post_liked(self.post.id, self.bob), False)

    def test_changing_a_like_to_a_dislike_keeps_a_single_row(self):
        PostService.update_post_like(self.bob, self.post.id, True)

        result = PostService.update_post_like(self.bob, self.post.id, False)

        self.assertEqual(result["like_count"], 0)
        self.assertEqual(result["dislike_count"], 1)
        self.assertEqual(PostLike.objects.filter(user=self.bob, post=self.post).count(), 1)

    def test_liking_twice_does_not_double_count(self):
        PostService.update_post_like(self.bob, self.post.id, True)

        result = PostService.update_post_like(self.bob, self.post.id, True)

        self.assertEqual(result["like_count"], 1)

    def test_counts_are_per_post_and_across_users(self):
        other_post = make_post(self.alice, "other")
        PostService.update_post_like(self.alice, self.post.id, True)
        PostService.update_post_like(self.bob, self.post.id, True)
        PostService.update_post_like(self.bob, other_post.id, False)

        self.assertEqual(PostService.get_like_count(self.post.id), 2)
        self.assertEqual(PostService.get_dislike_count(self.post.id), 0)
        self.assertEqual(PostService.get_like_count(other_post.id), 0)
        self.assertEqual(PostService.get_dislike_count(other_post.id), 1)

    def test_unlike_removes_the_reaction(self):
        PostService.update_post_like(self.bob, self.post.id, True)

        result = PostService.unlike_post(self.bob, self.post.id)

        self.assertTrue(result["success"])
        self.assertEqual(result["like_count"], 0)
        self.assertIsNone(PostService.is_post_liked(self.post.id, self.bob))

    def test_unlike_removes_a_dislike_too(self):
        PostService.update_post_like(self.bob, self.post.id, False)

        result = PostService.unlike_post(self.bob, self.post.id)

        self.assertEqual(result["dislike_count"], 0)

    def test_unlike_without_a_reaction_is_harmless(self):
        result = PostService.unlike_post(self.bob, self.post.id)

        self.assertTrue(result["success"])
        self.assertEqual(result["like_count"], 0)

    def test_unlike_only_removes_the_callers_reaction(self):
        PostService.update_post_like(self.alice, self.post.id, True)
        PostService.update_post_like(self.bob, self.post.id, True)

        result = PostService.unlike_post(self.bob, self.post.id)

        self.assertEqual(result["like_count"], 1)
        self.assertIs(PostService.is_post_liked(self.post.id, self.alice), True)

    def test_is_post_liked_is_none_without_a_reaction(self):
        self.assertIsNone(PostService.is_post_liked(self.post.id, self.bob))

    def test_actions_on_an_unknown_post_fail(self):
        self.assertFalse(PostService.update_post_like(self.bob, 999, True)["success"])
        self.assertFalse(PostService.unlike_post(self.bob, 999)["success"])


class PostFeedServiceTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.carol = make_user("carol")

    def test_all_posts_are_newest_first(self):
        old = make_post(self.alice, "old", age_minutes=30)
        new = make_post(self.bob, "new", age_minutes=1)
        mid = make_post(self.carol, "mid", age_minutes=10)

        self.assertEqual(list(PostService.get_all_posts()), [new, mid, old])

    def test_following_posts_contain_only_followed_users(self):
        UserService.follow_user(self.alice, "bob", True)
        bobs = make_post(self.bob, "from bob")
        make_post(self.carol, "from carol")
        make_post(self.alice, "from alice")

        self.assertEqual(list(PostService.get_following_posts(self.alice)), [bobs])

    def test_following_posts_are_empty_when_following_nobody(self):
        make_post(self.bob)

        self.assertEqual(list(PostService.get_following_posts(self.alice)), [])

    def test_following_posts_stop_after_unfollow(self):
        UserService.follow_user(self.alice, "bob", True)
        make_post(self.bob)
        UserService.follow_user(self.alice, "bob", False)

        self.assertEqual(list(PostService.get_following_posts(self.alice)), [])

    def test_user_posts_contain_only_that_users_posts(self):
        mine = make_post(self.alice, "mine")
        make_post(self.bob, "not mine")

        result = PostService.get_user_posts("alice")

        self.assertTrue(result["success"])
        self.assertEqual(list(result["posts"]), [mine])

    def test_user_posts_for_unknown_user_fails(self):
        result = PostService.get_user_posts("nobody")

        self.assertFalse(result["success"])

    # Known bug: the following and per-user feeds have no ordering, so they come
    # back oldest first while all posts is newest first. Remove the decorators
    # when fixed.
    @unittest.expectedFailure
    def test_following_posts_are_newest_first(self):
        UserService.follow_user(self.alice, "bob", True)
        old = make_post(self.bob, "old", age_minutes=30)
        new = make_post(self.bob, "new", age_minutes=1)

        self.assertEqual(list(PostService.get_following_posts(self.alice)), [new, old])

    @unittest.expectedFailure
    def test_user_posts_are_newest_first(self):
        old = make_post(self.alice, "old", age_minutes=30)
        new = make_post(self.alice, "new", age_minutes=1)

        result = PostService.get_user_posts("alice")

        self.assertEqual(list(result["posts"]), [new, old])


class ChatServiceTests(TestCase):
    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.carol = make_user("carol")
        self.chat = Chat.objects.create()
        self.chat.participants.add(self.alice, self.bob)

    def _send(self, sender, recipient, text):
        # The consumer stores one copy of every message per participant.
        for owner in (sender, recipient):
            ChatMessage.objects.create(
                user=owner, sender=sender, recipient=recipient, message=text, chat=self.chat
            )

    def test_get_chats_returns_only_chats_the_user_is_in(self):
        self.assertEqual(list(ChatService.get_chats(self.alice)), [self.chat])
        self.assertEqual(list(ChatService.get_chats(self.carol)), [])

    def test_unread_count_counts_incoming_messages_only(self):
        self._send(self.alice, self.bob, "one")
        self._send(self.alice, self.bob, "two")

        self.assertEqual(ChatService.get_unread_message_count(self.bob), 2)
        self.assertEqual(ChatService.get_unread_message_count(self.alice), 0)

    def test_set_messages_read_clears_the_unread_count(self):
        self._send(self.alice, self.bob, "one")

        ChatService.set_messages_read(self.chat, self.bob)

        self.assertEqual(ChatService.get_unread_message_count(self.bob), 0)

    def test_set_messages_read_does_not_touch_other_users_copies(self):
        self._send(self.alice, self.bob, "one")

        ChatService.set_messages_read(self.chat, self.alice)

        self.assertEqual(ChatService.get_unread_message_count(self.bob), 1)
