from datetime import timedelta

from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import Post, User

PASSWORD = "test-pass-123"


# Password hashing is deliberately slow; tests that do not log in with a
# password skip it, and the auth tests use FAST_HASHERS.
FAST_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


def make_user(username, password=None):
    """Create a user. Without a password the account has an unusable password."""
    return User.objects.create_user(
        username=username, email=f"{username}@example.com", password=password
    )


def make_post(user, text="hello", age_minutes=0):
    """Create a post and set date_created explicitly so ordering is deterministic.

    A larger age_minutes means an older post.
    """
    post = Post.objects.create(user=user, post=text)
    Post.objects.filter(pk=post.pk).update(
        date_created=timezone.now() - timedelta(minutes=age_minutes)
    )
    post.refresh_from_db()
    return post


def auth_client(user):
    """Return an APIClient authenticated as `user` with token auth.

    Server errors come back as 500 responses instead of being re-raised, so
    tests can assert on the status code.
    """
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.raise_request_exception = False
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client
