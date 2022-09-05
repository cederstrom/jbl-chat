import json

from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import Message, User


class ConversationTests(APITestCase):
    def setUp(self):
        User.objects.all().delete()
        Message.objects.all().delete()

        self.alpha = User.objects.create(username='alpha')
        self.bravo = User.objects.create(username='bravo')
        self.charlie = User.objects.create(username='charlie')

        self.message_a_to_c = Message.objects.create(content='a -> b', sender=self.alpha, receiver=self.bravo)
        Message.objects.create(content='b -> a', sender=self.bravo, receiver=self.alpha)
        Message.objects.create(content='a -> c', sender=self.alpha, receiver=self.charlie)

    def test_can_get_conversation_where_user_is_sender(self):
        self.client.force_authenticate(user=self.alpha)
        response = self.client.get('/conversation/charlie', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        message_contents = list(map(lambda message: message['content'], data))
        self.assertEqual(message_contents, ['a -> c'])

    def test_can_get_conversation_where_user_is_sender_or_receiver(self):
        self.client.force_authenticate(user=self.alpha)
        response = self.client.get('/conversation/bravo', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        message_contents = list(map(lambda message: message['content'], data))
        self.assertEqual(message_contents, ['b -> a', 'a -> b'])

    def test_can_send_message(self):
        foo = User.objects.create(username='foo')
        User.objects.create(username='bar')

        self.client.force_authenticate(user=foo)
        response = self.client.post('/conversation/bar', {'content': 'foo -> bar'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        message_contents = list(map(lambda message: message.content, Message.objects.filter(sender=foo)))
        self.assertEqual(message_contents, ['foo -> bar'])

    def test_messages_has_timestamp(self):
        self.client.force_authenticate(user=self.alpha)
        response = self.client.get('/conversation/charlie', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        timestamps = list(map(lambda message: message['datetime_sent'], data))
        timestamp_from_api = self.__datetime_str_without_milliseconds(timestamps[0])
        expected_timestamp = self.__datetime_str_without_milliseconds(self.message_a_to_c.datetime_sent.isoformat())
        self.assertEqual(timestamp_from_api, expected_timestamp)

    @staticmethod
    def __datetime_str_without_milliseconds(value):
        return value.split('.')[0]
