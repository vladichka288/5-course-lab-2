from .models import PhoneNumber, User
from .serializers import PhoneSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import database_sync_to_async
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)


def is_user_logged_in(user):
    return not isinstance(user, AnonymousUser)


@database_sync_to_async
def update_user_incr(user):
    if is_user_logged_in(user):
        User.objects.filter(pk=user.pk).update(online=True)


@database_sync_to_async
def update_user_decr(user):
    if is_user_logged_in(user):
        User.objects.filter(pk=user.pk).update(online=False)


class OnlineStatus:

    async def connect(self):
        await self.accept()
        await update_user_incr(self.scope['user'])

    async def disconnect(self, code):
        await update_user_decr(self.scope['user'])


class PhoneListView(OnlineStatus, GenericAsyncAPIConsumer, ListModelMixin):

    queryset = PhoneNumber.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = PhoneSerializer

    def get_queryset(self, **kwargs):
        phone_numbers = PhoneNumber.objects.filter(book_owner=self.scope['user']).order_by('name').values()
        return phone_numbers


class PhoneCreate(OnlineStatus, CreateModelMixin, GenericAsyncAPIConsumer):
    permission_classes = (IsAuthenticated, )
    serializer_class = PhoneSerializer

    def perform_create(self, serializer, **kwargs):
        return PhoneNumber.objects.create(name=serializer.data.get('name'), phone_number1=serializer.data.get('phone_number1'),
                                   phone_number2=serializer.data.get('phone_number2'), book_owner=self.scope['user'])


class PhoneDelete(OnlineStatus, GenericAsyncAPIConsumer, DeleteModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = PhoneSerializer

    def get_queryset(self, **kwargs):
        return PhoneNumber.objects.filter(book_owner=self.scope['user'])

