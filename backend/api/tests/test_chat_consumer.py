import unittest

from asgiref.sync import async_to_sync
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase, override_settings
from rest_framework.authtoken.models import Token

from api.models import Chat, ChatMessage
from api.routing import websocket_urlpatterns
from api.tests.helpers import make_user
from rest_twitter.channels_auth_middleware import TokenAuthMiddleware

IN_MEMORY_LAYER = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# Same stack as rest_twitter.asgi, minus the origin check (test clients send no Origin).
application = TokenAuthMiddleware(URLRouter(websocket_urlpatterns))


@override_settings(CHANNEL_LAYERS=IN_MEMORY_LAYER)
class ChatConsumerTests(TransactionTestCase):
    """Tests for api.consumers.ChatConsumer.

    The consumer is synchronous and uses the database from a worker thread, so
    these need TransactionTestCase rather than TestCase.

    Each test is a plain synchronous method that runs one async scenario with
    self.run_async() and then checks the database in ordinary sync code.
    Awaiting database_sync_to_async inside a scenario while the consumers are
    still running made the suite hang intermittently, so scenarios only
    exchange WebSocket messages and return what they received.
    """

    def setUp(self):
        self.alice = make_user("alice")
        self.bob = make_user("bob")
        self.alice_token = Token.objects.create(user=self.alice).key
        self.bob_token = Token.objects.create(user=self.bob).key
        self.communicators = []

    def run_async(self, scenario):
        """Run an async scenario, always closing its connections in the same event loop."""

        async def wrapped():
            try:
                return await scenario()
            finally:
                for communicator in self.communicators:
                    await communicator.disconnect()
                self.communicators = []

        return async_to_sync(wrapped)()

    async def connect(self, room, token=None):
        query = f"?token={token}" if token else ""
        communicator = WebsocketCommunicator(application, f"/ws/chat/{room}/{query}")
        connected, _ = await communicator.connect()
        if connected:
            self.communicators.append(communicator)
        return communicator, connected

    # --- connecting -------------------------------------------------------

    def test_user_can_connect_to_their_own_room(self):
        async def scenario():
            _, connected = await self.connect("alice", self.alice_token)
            return connected

        self.assertTrue(self.run_async(scenario))

    def test_anonymous_connection_is_rejected(self):
        async def scenario():
            _, connected = await self.connect("alice")
            return connected

        self.assertFalse(self.run_async(scenario))

    def test_invalid_token_is_rejected(self):
        async def scenario():
            _, connected = await self.connect("alice", "not-a-real-token")
            return connected

        self.assertFalse(self.run_async(scenario))

    def test_user_cannot_connect_to_someone_elses_room(self):
        async def scenario():
            _, connected = await self.connect("alice", self.bob_token)
            return connected

        self.assertFalse(self.run_async(scenario))

    # --- sending ----------------------------------------------------------

    def test_message_is_delivered_to_sender_and_recipient(self):
        async def scenario():
            alice, _ = await self.connect("alice", self.alice_token)
            bob, _ = await self.connect("bob", self.bob_token)
            await alice.send_json_to({"chat": None, "recipient": "bob", "message": "hi bob"})
            return await alice.receive_json_from(), await bob.receive_json_from()

        sent, received = self.run_async(scenario)

        self.assertEqual(sent["message"]["message"], "hi bob")
        self.assertFalse(sent["message"]["incoming"])
        self.assertTrue(sent["is_chat_new"])
        self.assertEqual(received["message"]["message"], "hi bob")
        self.assertTrue(received["message"]["incoming"])
        self.assertEqual(received["message"]["sender"], "alice")
        self.assertEqual(received["message"]["recipient"], "bob")
        self.assertEqual(received["chat"], sent["chat"])

    def test_message_is_stored_once_per_participant(self):
        async def scenario():
            alice, _ = await self.connect("alice", self.alice_token)
            bob, _ = await self.connect("bob", self.bob_token)
            await alice.send_json_to({"chat": None, "recipient": "bob", "message": "hi bob"})
            await alice.receive_json_from()
            await bob.receive_json_from()

        self.run_async(scenario)

        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(ChatMessage.objects.filter(user=self.alice).count(), 1)
        self.assertEqual(ChatMessage.objects.filter(user=self.bob).count(), 1)

    def test_recipient_has_an_unread_message(self):
        async def scenario():
            alice, _ = await self.connect("alice", self.alice_token)
            bob, _ = await self.connect("bob", self.bob_token)
            await alice.send_json_to({"chat": None, "recipient": "bob", "message": "hi bob"})
            await alice.receive_json_from()
            return await bob.receive_json_from()

        received = self.run_async(scenario)

        self.assertEqual(received["total_unread_count"], 1)
        unread = ChatMessage.objects.filter(user=self.bob, recipient=self.bob, read=False)
        self.assertEqual(unread.count(), 1)

    def test_follow_up_messages_reuse_the_chat(self):
        async def scenario():
            alice, _ = await self.connect("alice", self.alice_token)
            bob, _ = await self.connect("bob", self.bob_token)
            await alice.send_json_to({"chat": None, "recipient": "bob", "message": "one"})
            first = await alice.receive_json_from()
            await bob.receive_json_from()
            await bob.send_json_to({"chat": first["chat"], "recipient": "alice", "message": "two"})
            reply = await bob.receive_json_from()
            await alice.receive_json_from()
            return first, reply

        first, reply = self.run_async(scenario)

        self.assertFalse(reply["is_chat_new"])
        self.assertEqual(reply["chat"], first["chat"])
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(ChatMessage.objects.filter(user=self.alice).count(), 2)

    def test_message_to_an_unknown_user_returns_an_error(self):
        async def scenario():
            alice, _ = await self.connect("alice", self.alice_token)
            await alice.send_json_to({"chat": None, "recipient": "nobody", "message": "hello?"})
            return await alice.receive_json_from()

        response = self.run_async(scenario)

        self.assertEqual(response, {"error": "The user does not exist"})
        self.assertEqual(ChatMessage.objects.count(), 0)

    # --- known bug --------------------------------------------------------

    # Known bug: when connect() rejects a connection it never sets
    # room_group_name, so disconnect() raises AttributeError for every rejected
    # connection. Remove the decorator when fixed.
    @unittest.expectedFailure
    def test_rejected_connection_disconnects_cleanly(self):
        async def scenario():
            communicator = WebsocketCommunicator(application, "/ws/chat/alice/")
            connected, _ = await communicator.connect()
            self.assertFalse(connected)
            await communicator.disconnect()

        self.run_async(scenario)
