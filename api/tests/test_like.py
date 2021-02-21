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
        self.post = baker.make('Post')

    
    def authorize_client(self):
        url = reverse('api_login')
        response = self.client.post(url, self.data, format='json')
        self.client = APIClient()
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_like_create(self):
        self.authorize_client()
        url = reverse('api_create_like', args=[self.post.pk])
        data = {'post': self.post.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().post, self.post)

    
    def test_like_delete(self):
        self.authorize_client()
        url = reverse('api_create_like', args=[self.post.pk])
        data = {'post': self.post.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api_delete_like', args=[self.post.pk])
        data = {'post': self.post.pk}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)