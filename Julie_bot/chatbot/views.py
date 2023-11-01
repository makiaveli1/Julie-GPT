from django.shortcuts import render, redirect
from django.http import JsonResponse
import autogen
import os
from dotenv import load_dotenv
from Prompt import julie_description  
import logging
from django.contrib import auth
from django.contrib.auth.models import User

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv('keys.env')

autogen_config = {
    "model": "gpt-4-0613",
    "max_tokens": 4000,
    "temperature": 0.7,
    "top_p": 0.8,  # Added top_p for more control over output diversity
    "presence_penalty": 0.2,
    "frequency_penalty": 0.5,
    "api_key": os.getenv("OPENAI_API_KEY"),
    "api_type": "open_ai",
    "api_base": "https://api.openai.com/v1",
}

def get_prompt(user_input, context=None):
    # Using a format string for more dynamic prompt construction
    prompt = f"The following is a conversation with Julie, a personal assistant. {julie_description}" 
    prompt += f"\n\nHuman: {user_input}"
    if context:
        prompt += f"\nContext: {context}"
    prompt += "\n\nJulie: "
    return prompt

def chatbot_logic(user_input, context=None):
    prompt = get_prompt(user_input, context)
    try:
        # Making the API call within a try block to handle potential errors
        response = autogen.ChatCompletion.create(prompt=prompt, **autogen_config)
        logging.info(f"Request to autogen: {prompt}")  
        return autogen.ChatCompletion.extract_text(response)[0]
    except Exception as e:
        logging.error(f"An error occurred while communicating with autogen: {e}")
        return "An error occurred while processing your request."


def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        response = chatbot_logic(user_input)
        return JsonResponse({'message': user_input, 'response': response})
    return render(request, 'chatbot.html')


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
    return render(request, 'login.html')