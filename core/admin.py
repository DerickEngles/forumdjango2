from django.contrib import admin
from .models import Register


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('photo', 'name', 'status', 'slug', 'creation', 'modification', 'active')
