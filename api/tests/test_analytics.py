from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import User, Post, Like


class LikeTests(APITestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, email='user@e.com', password=self.password)
        self.data = {
            'username': self.username,
            'password': self.password
        }
        self.like = baker.make('Like')


    def authorize_client(self):
        url = reverse('api_login')
        response = self.client.post(url, self.data, format='json')
        self.client = APIClient()
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    
    def test_analytics(self):
        self.authorize_client()
        url = reverse('api_analytics') 
        response = self.client.get(url, {'date_from': '2021-01-01', 'date_to': '2021-12-01'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['liked_count'], 1)