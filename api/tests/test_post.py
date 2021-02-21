from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import User, Post


class PostTests(APITestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, email='user@e.com', password=self.password)
        self.data = {
            'username': self.username,
            'password': self.password
        }
        self.post_data = {
            'title': 'title',
            'text': 'text'
        }
        

    def authorize_client(self):
        url = reverse('api_login')
        response = self.client.post(url, self.data, format='json')
        self.client = APIClient()
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_post_create(self):
        self.authorize_client()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post('/api/posts/', data=self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'title')
        self.assertEqual(post.text, 'text')
        self.assertEqual(post.created_by, self.user)


    def test_post_delete(self):
        self.authorize_client()
        response = self.client.delete('/api/posts/28')
        self.assertEqual(response.status_code, 404)
        
        post = baker.make('Post')
        response = self.client.delete('/api/posts/' + str(post.id))
        self.assertEqual(response.status_code, 204)

