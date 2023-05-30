import os
import jwt
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'directory.settings')
django.setup()
from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings
from .models import User



ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except:
        return AnonymousUser()
    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        return AnonymousUser()
    return user


class TokenMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            jwt_key = [item for item in scope['headers'] if b'authorization' in item][0][1].decode('utf-8')
        except ValueError:
            jwt_key = None
        scope['user'] = await get_user(jwt_key)
        return await super().__call__(scope, receive, send)


def JwtMiddleware(inner):
    return TokenMiddleware(inner)
