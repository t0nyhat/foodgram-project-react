from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "first_name", "last_name", "email")
    list_filter = ("username", "email")


admin.site.register(User, UserAdmin)


@admin.register(Follow)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("author", "follower")
