from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from chat.models import User


class UsersTests(APITestCase):
    def test_users_resource_is_protected(self):
        response = self.client.get('/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_fetch_users(self):
        user = User.objects.create(username='olivia')
        self.client.force_authenticate(user=user)
        response = self.client.get('/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'[{"username":"olivia"}]')
