from django.urls import path
from django.shortcuts import redirect
from . import views
from .import views

urlpatterns = [
    path('', lambda request: redirect('chatbot', permanent=False)),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('get-profile-data/', views.get_profile_data, name='get_profile_data'),
    path('message_sent/', views.chatbot_message_sent,
         name='chatbot_message_sent'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
