from django.urls import path
from .import views

urlpatterns = [
  path('', views.chatbot, name='chatbot'),
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('logout/', views.logout, name='logout'),
  path('update-profile/', views.update_profile, name='update_profile'),
  path('get-profile-data/', views.get_profile_data, name='get_profile_data')
]
