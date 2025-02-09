from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "phone",
        "password",
        "created_at",
        "updated_at",
        "suspended_at",
    ]
    list_filter = [
        "created_at",
    ]
    search_fields = ["username", "phone", "id"]