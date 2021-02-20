from django.urls import path, include
from .views import (
    LoginView, 
    RegisterView, 
    PostViewSet, 
    UserViewSet,
    create_like,
    delete_like,
    analytics,
    Activity
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name = 'api_login'),
    path('register/', RegisterView.as_view(), name = 'api_register'),
    path('login/refresh/', TokenRefreshView.as_view(), name = 'api_token_refresh'),
    path('posts/like/<int:post_id>', create_like, name='api_create_like'),
    path('posts/delete_like/<int:like_id>', delete_like, name='api_delete_like'),
    path('analytics/', analytics, name='api_analytics'),
    path('activity/<int:pk>', Activity.as_view(), name='api_activity'),
]

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
urlpatterns += router.urls
