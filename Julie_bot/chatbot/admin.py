from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Chat

# Register your models here.
admin.site.register(Chat)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'bio', 'profile_picture']

admin.site.register(CustomUser, CustomUserAdmin)