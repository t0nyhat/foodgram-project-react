from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow
from .paginator import Paginator
from .serializers import FollowerSerializer, FollowSerializer, UserSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = Paginator
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = Follow.objects.filter(follower=request.user)
        page = self.paginate_queryset(queryset)
        recipes_limit = request.GET.get('recipes_limit', default=None)
        serializer = FollowerSerializer(
            page, many=True, context={'recipes_limit': recipes_limit}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        follower = request.user
        author = get_object_or_404(User, id=id)
        data = {
            'follower': follower.id,
            'author': author.id
        }
        serializer = FollowSerializer(
            data=data, context={'request': request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        queryset = Follow.objects.filter(follower=request.user, author=author)
        serializer = FollowerSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        follower = request.user
        author = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(
            Follow, follower=follower, author=author
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
