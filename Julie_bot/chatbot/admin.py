from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Chat

# Register your models here.
admin.site.register(Chat)
admin.site.register(CustomUser, UserAdmin)
