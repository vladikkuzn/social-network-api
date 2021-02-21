from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import User, Post


class UserTests(APITestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.data = {
            'username': self.username,
            'password': self.password
        }
        self.post = baker.make('Post')

    def test_user(self):
        # test user creation inside db
        user = User.objects.create_user(username=self.username, email='user@e.com', password=self.password)
        self.assertEqual(user.is_active, 1, 'Active User')
        
        # test login route
        url = reverse('api_login')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        
        # test JWT authorization
        client = APIClient()
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get('/api/posts/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)