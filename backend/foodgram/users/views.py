from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .paginator import Paginator
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = Paginator
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
