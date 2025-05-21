"""
ASGI config for rest_twitter project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

"""
ASGI config for project4 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
django.setup()
from channels.security.websocket import AllowedHostsOriginValidator
from .channels_auth_middleware import TokenAuthMiddleware
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_twitter.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                api.routing.websocket_urlpatterns
            )
        )
    )
})


