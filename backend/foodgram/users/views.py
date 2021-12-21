from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from .paginator import Paginator
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = Paginator
    queryset = User.objects.all()
    serializer_class = UserSerializer
