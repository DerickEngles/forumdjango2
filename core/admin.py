from django.contrib import admin
from .models import Register, Post


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'username', 'email', 'password', 'status', 'slug', 'date_joined', 'modification',
                    'is_active')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'photo', 'user', 'title', 'subject', 'text', 'slug')
