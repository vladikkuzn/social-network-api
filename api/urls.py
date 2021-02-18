from django.urls import path, include
from .views import LoginView, RegisterView, PostViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('login/', LoginView.as_view(), name = 'api_login'),
    path('register/', RegisterView.as_view(), name = 'api_register'),
    path('login/refresh/', TokenRefreshView.as_view(), name = 'api_token_refresh'),

]

urlpatterns += router.urls