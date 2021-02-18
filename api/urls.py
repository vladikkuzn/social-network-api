from django.urls import path
from api.views import LoginView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name = 'api_login'),
    path('register/', RegisterView.as_view(), name = 'api_register'),
    path('login/refresh/', TokenRefreshView.as_view(), name = 'api_token_refresh')
]