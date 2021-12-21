from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
]
