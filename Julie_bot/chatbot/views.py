from .models import Chat, CustomUser
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils import timezone
from dotenv import load_dotenv
import os
import logging
from .Juliebot import Juliebot
from .brain import LongTermMemory

logger = logging.getLogger(__name__)

load_dotenv('keys.env')

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_username = os.getenv("REDIS_USER")
redis_password = os.getenv("REDIS_PASS")



@login_required
def chatbot(request):
    if not request.user.is_authenticated:
        # Handle unauthenticated users
        return redirect('login')  # Redirect to login page

    # For GET requests, render the chatbot page with chat history
    if request.method == 'GET':
        chats = Chat.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'chatbot.html', {'chats': chats})

    # For POST requests, process the chat message
    elif request.method == 'POST':
        user_input = request.POST.get('message')
        logger.error(f"User input retrieved from POST request: '{user_input}'")
        username = request.user.username

        # Validate user input
        if not user_input or not user_input.strip():
            # Return a bad request response for invalid input
            return HttpResponseBadRequest("Invalid or empty message.")

        try:
            # Initialize Juliebot and generate response
            long_term_memory = LongTermMemory(redis_host, redis_port, redis_username, redis_password)
            julie_bot = Juliebot(long_term_memory=long_term_memory)
            julie_bot.start_conversation(username)
            response = julie_bot.generate_response(username, user_input)
            logger.error(f"Response generated from Juliebot: '{response}'")

            # Save the chat to the database
            Chat.objects.create(user=request.user, message=user_input, response=response, created_at=timezone.now())

        except Exception as e:
            logger.error(f"Error in generating chat response: {e}")
            # Return a generic error message to the user
            return JsonResponse({'message': user_input, 'response': "Sorry, there was an error processing your request."})

        # Return the JsonResponse with the message and response
        return JsonResponse({'message': user_input, 'response': response})

    else:
        # Handle other HTTP methods
        return HttpResponseBadRequest("Unsupported request method.")



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
                user = CustomUser.objects.create_user(username, email, password1)
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        # Get the custom user's profile
        user = request.user

        # Update the user's name, email, and other fields
        user.first_name = request.POST.get('full_name', user.first_name)
        user.email = request.POST.get('email', user.email)

        # Only update the password if it's provided
        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])

        # Assume additional fields like phone, bio, social_media are part of the User model
        # This requires custom user model which extends the built-in User model
        user.phone = request.POST.get('phone', user.phone)
        user.bio = request.POST.get('bio', user.bio)
        user.social_media = request.POST.get('social_media', user.social_media)

        # Handle the profile picture upload
        if 'profile_picture' in request.FILES:
            file = request.FILES['profile_picture']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            user.profile_picture = fs.url(filename)

        user.save()

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully.'})
    else:
        # If it's not a POST request, return an error response
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def logout(request):
    auth.logout(request)
    return render(request, 'chatbot.html')