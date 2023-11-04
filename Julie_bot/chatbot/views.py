from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Chat
from django.utils import timezone
from dotenv import load_dotenv
import os
from .Juliebot import Juliebot
from .brain import LongTermMemory


load_dotenv('keys.env')

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_username = os.getenv("REDIS_USER")
redis_password = os.getenv("REDIS_PASS")


# Setup logging
@login_required
def chatbot(request):
    # Initialize chats as empty for all cases
    chats = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user).order_by('-created_at')

        # Initialize an instance of LongTermMemory (you need to replace the parameters with the actual values or environment variables)
        long_term_memory = LongTermMemory(redis_host, redis_port, redis_username, redis_password)

        if request.method == 'POST':
            user_input = request.POST.get('message')
            username = request.user.username

            # Initialize Juliebot with LongTermMemory
            julie_bot = Juliebot(long_term_memory=long_term_memory)
            julie_bot.start_conversation(username)  # Initialize conversation history

            # Generate a response using the chatbot_logic method
            response = julie_bot.generate_response(username, user_input) 
            
            # Save the chat to the database
            chat = Chat(user=request.user, message=user_input, response=response, created_at=timezone.now())
            chat.save()
            
            # Return the JsonResponse with the message and response
            return JsonResponse({'message': user_input, 'response': response})

    else:
        # Handle unauthenticated users - Redirect to login page or show an error
        return redirect('login')  # Assuming you have a login view named 'login'

    # Render the chatbot page with the chats context
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