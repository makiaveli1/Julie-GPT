import autogen
import os
from dotenv import load_dotenv
from Prompt import julie_description  
import logging

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

class Juliebot:
    
    def __init__(self):
        pass

    def get_prompt(self, user_input, context=None):
        # Using a format string for more dynamic prompt construction
        prompt = f"The following is a conversation with Julie, a personal assistant. {julie_description}" 
        prompt += f"\n\nHuman: {user_input}"
        if context:
            prompt += f"\nContext: {context}"
        prompt += "\n\nJulie: "
        return prompt

    def chatbot_logic(self, user_input, context=None):
        prompt = self.get_prompt(user_input, context)
        try:
            # Making the API call within a try block to handle potential errors
            response = autogen.ChatCompletion.create(prompt=prompt, **autogen_config)
            logging.info(f"Request to autogen: {prompt}")  
            return autogen.ChatCompletion.extract_text(response)[0]
        except Exception as e:
            logging.error(f"An error occurred while communicating with autogen: {e}")
            return "An error occurred while processing your request."

