from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import User, Post, Like
import datetime


class LikeTests(APITestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, email='user@e.com', password=self.password)
        self.data = {
            'username': self.username,
            'password': self.password
        }


    def authorize_client(self):
        url = reverse('api_login')
        response = self.client.post(url, self.data, format='json')
        self.client = APIClient()
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_activity(self):
        self.authorize_client()
        url = reverse('api_activity', kwargs={'pk': self.user.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_login'], None)
        self.assertEqual(response.data['last_request'][:10], str(datetime.datetime.today())[:10])