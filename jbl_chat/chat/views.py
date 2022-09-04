from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from chat.models import Message, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'sender', 'receiver']
        read_only_fields = ['sender', 'receiver']


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def create(self, request, username):
        receiver = User.objects.get(username=username)
        sender = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender, receiver=receiver)
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        me = self.request.user
        other_user = User.objects.get(username=self.kwargs['username'])
        return Message.objects.filter(sender=other_user, receiver=me) | \
               Message.objects.filter(sender=me, receiver=other_user)
