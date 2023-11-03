from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Chat
from django.utils import timezone
from .Juliebot import Juliebot

# Setup logging
@login_required
def chatbot(request):
    # Initialize chats as empty for all cases
    chats = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user).order_by('-created_at')
        
        if request.method == 'POST':
            user_input = request.POST.get('message')
            username = request.user.username  # Retrieve the username
            response = Juliebot().chatbot_logic(user_input, username=username)  
            chat = Chat(user=request.user, message=user_input, response=response, created_at=timezone.now())
            chat.save()
            return JsonResponse({'message': user_input, 'response': response})

    else:
        # Handle unauthenticated users - Redirect to login page or show an error
        return redirect('login')  # Assuming you have a login view named 'login'

    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Username already taken'
                return render(request, 'register.html', {'error': error_message})
        else:
            error_message = 'Passwords must match'
            return render(request, 'register.html', {'error': error_message})
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return render(request, 'chatbot.html')