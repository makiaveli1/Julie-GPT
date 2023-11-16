from .models import Chat, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils import timezone
from .Juliebot import Juliebot
from .brain import LongTermMemory
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

# Initialize the Redis and Juliebot configurations outside the view function
# Now pulling configuration from Django's settings
redis_config = {
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
    'username': settings.REDIS_USER,
    'password': settings.REDIS_PASS
}
long_term_memory = LongTermMemory(redis_config)
julie_bot = Juliebot(long_term_memory)


@login_required
def chatbot(request):
    if request.method == 'GET':
        chat_session, created = Chat.objects.get_or_create(user=request.user)
        return render(request, 'chatbot.html', {'chat_session': chat_session})

    elif request.method == 'POST':
        user_input = request.POST.get('message')
        username = request.user.username

        if not user_input or not user_input.strip():
            return HttpResponseBadRequest("Invalid or empty message.")

        try:
            julie_bot.send_message(user_input, username)
            response = julie_bot.run_assistant(username)

            chat_session = Chat.objects.get(user=request.user)
            chat_history = chat_session.messages
            timestamp = timezone.now().strftime("%Y-%m-%dT%H:%M:%S")
            chat_history.append({'role': 'user', 'message': user_input, 'timestamp': timestamp})
            chat_history.append({'role': 'assistant', 'message': response, 'timestamp': timestamp})
            chat_session.messages = chat_history
            chat_session.save()
        except Exception as e:
            logger.error(f"Error in generating chat response: {e}")
            return JsonResponse({'message': user_input, 'response': "Sorry, there was an error processing your request."})

        return JsonResponse({'message': user_input, 'response': response})

    else:
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