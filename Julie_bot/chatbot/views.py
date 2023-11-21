from .models import Chat, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils import timezone
from cloudinary.uploader import upload
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
            chat_history.append({'role': 'user', 'message': user_input,
                                 'timestamp': timestamp})
            chat_history.append({'role': 'assistant', 'message': response,
                                 'timestamp': timestamp})
            chat_session.messages = chat_history
            chat_session.save()
        except Exception as e:
            logger.error(f"Error in generating chat response: {e}")
            return JsonResponse({'message': user_input, 'response':
                                 """Sorry, there was an error processing
                                 your request."""})

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
                user = CustomUser.objects.create_user(username, email,
                                                      password1, bio)
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
        user = request.user

        # Update basic profile information only if new value is provided
        full_name = request.POST.get('full_name')
        if full_name is not None:
            user.first_name = full_name

        last_name = request.POST.get('last_name')
        if last_name is not None:
            user.last_name = last_name

        username = request.POST.get('user_name')
        if username is not None:
            user.username = username

        email = request.POST.get('email')
        if email is not None:
            user.email = email

        phone = request.POST.get('phone')
        if phone is not None:
            user.phone = phone

        bio = request.POST.get('bio')
        if bio is not None:
            user.bio = bio

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            try:
                uploaded_file = request.FILES['profile_picture']
                # Make sure the 'upload' function works correctly
                upload_result = upload(uploaded_file)
                user.profile_picture_url = upload_result.get('url')
            except Exception as e:
                # Handle exceptions that may occur during file upload
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        # Save the user model after making changes
        user.save()

        # Respond with success message
        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully.'})
    else:
        # Handle incorrect request method
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def get_profile_data(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Invalid request method.")

    user = request.user
    # Assuming you have a method or a field in CustomUser for profile picture URL
    profile_picture_url = getattr(user, 'profile_picture_url', None)

    # Construct full name manually if get_full_name() doesn't give desired results
    full_name = user.get_full_name() or f"{user.first_name} {user.last_name}".strip()

    profile_data = {
        'status': 'success',
        'full_name': full_name,
        'username': user.username,
        'email': user.email,
        'phone': user.phone or '',
        'bio': user.bio or '',
        'social_media': getattr(user, 'social_media', ''),
        'profile_picture': profile_picture_url
    }

    return JsonResponse(profile_data)


def logout(request):
    auth.logout(request)
    return render(request, 'chatbot.html')
