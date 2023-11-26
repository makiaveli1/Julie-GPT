from .models import Chat, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from cloudinary.uploader import upload
from .Juliebot import Juliebot
from .brain import LongTermMemory
from django.conf import settings
from django.utils.formats import date_format
import uuid
import logging
import hashlib

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
        chat_session.refresh_from_db()
        return render(request, 'chatbot.html', {'chat_session': chat_session})

    elif request.method == 'POST':
        user_input = request.POST.get('message').strip()
        username = request.user.username
        # Expecting a unique ID from the client
        client_message_id = request.POST.get('client_message_id', None)

        if not user_input or not client_message_id:
            return HttpResponseBadRequest("Invalid or empty message or missing message ID.")

        # Attempt to prevent processing the same message twice by checking for client_message_id
        with transaction.atomic():
            chat_session, created = Chat.objects.select_for_update().get_or_create(user=request.user)
            if any(msg.get('client_message_id') == client_message_id for msg in chat_session.messages):
                # If the message ID is found, it's a duplicate; don't process it again
                return JsonResponse({'status': 'info', 'message': 'Message already processed.'})

            try:
                julie_bot.send_message(user_input, username)
                response = julie_bot.run_assistant(username)

                # Format the timestamp to show time only
                # This will format the time to HH:MM format
                time_only = timezone.localtime().strftime('%H:%M')

                user_message = {
                    'role': 'user',
                    'message': user_input,
                    'timestamp': time_only,
                    'client_message_id': client_message_id
                }
                bot_message = {
                    'role': 'assistant',
                    'message': response,
                    'timestamp': time_only,
                    'id': uuid.uuid4().hex
                }

                chat_history = chat_session.messages
                chat_history.extend([user_message, bot_message])
                chat_session.save()

            except Exception as e:
                logger.error(f"Error in generating chat response: {e}")
                return JsonResponse({'status': 'error',
                                     'message': """Sorry,
                                     there was an error processing your
                                     request."""})

            return JsonResponse({
                'status': 'success',
                'response': response,
                'timestamp': time_only,
                'message_id': uuid.uuid4().hex
            })

    else:
        return HttpResponseBadRequest("Unsupported request method.")


@login_required
def chatbot_message_sent(request):
    """
    View to redirect to after a message is sent to prevent resubmission upon refresh.
    This view can either show a confirmation message or redirect back to the chat page where 
    the messages can be fetched and displayed. For the purpose of preventing form resubmission,
    it simply redirects back to the main chat view.
    """
    # You can optionally add any logic here if you need to process anything
    # before redirecting back to the chat view. For instance, you could set a
    # session variable, flash a message, or log an event.

    # Redirect back to the main chat view, which will show the chat session,
    # including the message that was just sent.
    return redirect('chatbot')


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
                                                      password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Username already taken'
                return render(request,
                              'register.html', {'error': error_message})
        else:
            error_message = 'Passwords must match'
            return render(request, 'register.html', {'error': error_message})
    return render(request, 'register.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user

        # Update basic profile information only if new value is provided
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if first_name is not None:
            user.first_name = first_name
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
                return JsonResponse({'status': 'error',
                                     'message': str(e)}, status=400)

        # Save the user model after making changes
        user.save()

        # Respond with success message
        return JsonResponse({'status': 'success',
                             'message': 'Profile updated successfully.'})
    else:
        # Handle incorrect request method
        return JsonResponse({'status': 'error',
                             'message': 'Invalid request method'}, status=400)


@login_required
def get_profile_data(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Invalid request method.")

    user = request.user
    # Assuming you have a method or
    # a field in CustomUser for profile picture URL
    profile_picture_url = getattr(user, 'profile_picture_url', None)

    # Construct full name manually if
    # get_full_name() doesn't give desired results
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


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, 'Your account has been deleted.')
    return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('login')
