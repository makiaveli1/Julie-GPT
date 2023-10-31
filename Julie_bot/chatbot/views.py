from django.shortcuts import render
from django.http import JsonResponse
import openai

# Create your views here.
def openai_request(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        
        answer = response['choices'][0]['message']['content']
        return answer.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def chatbot(request):

    if request.method == 'POST':
        message = request.POST.get('message')
        response = openai_request(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')