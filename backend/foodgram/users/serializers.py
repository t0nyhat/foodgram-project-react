from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username",
                  "first_name", "last_name", "password")

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Данный username не разрешен, выберите другой')
        return value


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return False


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    author = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('author', 'follower'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate_following(self, user):
        if user == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return user
