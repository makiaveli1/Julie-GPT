from .models import Chat, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db import IntegrityError
from cloudinary.uploader import upload
from .Juliebot import Juliebot
from .brain import LongTermMemory
from django.conf import settings
import uuid
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


@login_required(login_url='/login/')
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
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if either field is empty and return an appropriate message
        if not username or not password:
            error_message = 'Username and password cannot be empty.'
            return JsonResponse({"error": error_message}, status=400)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": True})
                return redirect('chatbot')
            else:
                error_message = 'Your account has been disabled. So sad.'
        else:
            error_message = 'Invalid username or password. Please try again.'

        # Handle AJAX and non-AJAX requests differently
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"error": error_message}, status=400)
        else:
            messages.error(request, error_message)

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if not username or not email or not password1 or not password2:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        try:
            user = CustomUser.objects.create_user(username, email, password1)
            user.save()
            auth.login(request, user)
            # Check for AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": "User created and logged in."}, status=200)
            return redirect('chatbot')
        except IntegrityError:
            messages.error(request, 'Username already taken.')
        except Exception as e:
            messages.error(
                request, 'An unexpected error occurred. Please try again.')

    # Check for AJAX request for error handling
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"errors": dict(messages.get_messages(request))}, status=400)
    return render(request, 'register.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user

        # Update fields only if they are provided in the request
        if 'first_name' in request.POST:
            user.first_name = request.POST.get('first_name')

        if 'last_name' in request.POST:
            user.last_name = request.POST.get('last_name')

        if 'email' in request.POST:
            user.email = request.POST.get('email')

        if 'phone' in request.POST:
            user.phone = request.POST.get('phone')

        if 'bio' in request.POST:
            user.bio = request.POST.get('bio')

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            try:
                uploaded_file = request.FILES['profile_picture']
                # Ensure your upload function works correctly
                upload_result = upload(uploaded_file)
                user.profile_picture_url = upload_result.get('url')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        user.save()

        # Return updated user data
        updated_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'bio': user.bio,
            'profile_picture_url': user.profile_picture_url
        }

        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully.', 'data': updated_data})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


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
    full_name = user.get_full_name() or f"""{user.first_name} {
        user.last_name}""".strip()

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
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('login')
    return HttpResponseBadRequest("Invalid request method.")


def logout(request):
    auth.logout(request)
    return redirect('login')
