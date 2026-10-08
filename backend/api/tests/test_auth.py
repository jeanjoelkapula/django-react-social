from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import User
from api.tests.helpers import FAST_HASHERS, PASSWORD, auth_client, make_user


@override_settings(PASSWORD_HASHERS=FAST_HASHERS)
class RegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/auth/register/"

    def test_register_creates_user_and_returns_token(self):
        response = self.client.post(
            self.url,
            {"username": "alice", "email": "alice@example.com", "password": PASSWORD},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["auth"]["user"]["username"], "alice")
        user = User.objects.get(username="alice")
        self.assertEqual(data["auth"]["token"], Token.objects.get(user=user).key)

    def test_register_stores_a_hashed_password(self):
        self.client.post(
            self.url,
            {"username": "alice", "email": "alice@example.com", "password": PASSWORD},
            format="json",
        )

        user = User.objects.get(username="alice")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))

    def test_register_duplicate_username_returns_errors_and_creates_nothing(self):
        make_user("alice")

        response = self.client.post(
            self.url,
            {"username": "alice", "email": "other@example.com", "password": PASSWORD},
            format="json",
        )

        self.assertIn("username", response.json()["errors"])
        self.assertEqual(User.objects.filter(username="alice").count(), 1)

    def test_register_requires_a_password(self):
        response = self.client.post(
            self.url, {"username": "alice", "email": "a@example.com"}, format="json"
        )

        self.assertIn("password", response.json()["errors"])
        self.assertFalse(User.objects.filter(username="alice").exists())


@override_settings(PASSWORD_HASHERS=FAST_HASHERS)
class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/auth/login/"
        self.user = make_user("alice", PASSWORD)

    def test_login_returns_user_details_and_token(self):
        response = self.client.post(
            self.url, {"username": "alice", "password": PASSWORD}, format="json"
        )

        data = response.json()
        self.assertEqual(data["auth"]["user"]["username"], "alice")
        self.assertEqual(data["auth"]["token"], Token.objects.get(user=self.user).key)

    def test_login_reuses_the_existing_token(self):
        first = self.client.post(
            self.url, {"username": "alice", "password": PASSWORD}, format="json"
        ).json()
        second = self.client.post(
            self.url, {"username": "alice", "password": PASSWORD}, format="json"
        ).json()

        self.assertEqual(first["auth"]["token"], second["auth"]["token"])

    def test_login_with_wrong_password_is_rejected(self):
        response = self.client.post(
            self.url, {"username": "alice", "password": "wrong"}, format="json"
        )

        data = response.json()
        self.assertEqual(data["errors"]["messages"], ["Invalid credentials"])
        self.assertNotIn("auth", data)

    def test_login_with_unknown_user_is_rejected(self):
        response = self.client.post(
            self.url, {"username": "nobody", "password": PASSWORD}, format="json"
        )

        self.assertEqual(response.json()["errors"]["messages"], ["Invalid credentials"])

    def test_login_requires_username_and_password(self):
        response = self.client.post(self.url, {}, format="json")

        errors = response.json()["errors"]
        self.assertIn("username", errors)
        self.assertIn("password", errors)


class LogoutAndAuthenticationTests(TestCase):
    def test_logout_invalidates_the_token(self):
        user = make_user("alice")
        client = auth_client(user)
        self.assertEqual(client.get("/api/posts/").status_code, 200)

        response = client.get("/api/auth/logout/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(user=user).exists())
        self.assertEqual(client.get("/api/posts/").status_code, 401)

    def test_protected_endpoints_require_authentication(self):
        client = APIClient()
        cases = [
            ("get", "/api/posts/"),
            ("get", "/api/posts/following/"),
            ("get", "/api/alice/posts/"),
            ("get", "/api/alice/profile/"),
            ("get", "/api/chats/"),
            ("post", "/api/post/"),
            ("put", "/api/alice/follow/"),
            ("put", "/api/post/1/like/"),
            ("put", "/api/post/1/unlike/"),
        ]
        for method, url in cases:
            with self.subTest(method=method, url=url):
                response = getattr(client, method)(url, format="json")
                self.assertEqual(response.status_code, 401)

    def test_invalid_token_is_rejected(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token not-a-real-token")

        self.assertEqual(client.get("/api/posts/").status_code, 401)
