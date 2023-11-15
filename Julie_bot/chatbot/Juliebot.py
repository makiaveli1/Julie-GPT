import os
import autogen
from dotenv import load_dotenv
from Prompt import julie_description
import logging
from .brain import LongTermMemory


logger = logging.getLogger(__name__)

autogen_config = {
"model": "gpt-4-1106-preview",
"max_tokens": 4000,
"temperature": 0.65,
"top_p": 0.8,
"presence_penalty": 0.2,
"frequency_penalty": 0.5,
"api_key": os.getenv("OPENAI_API_KEY"),
"api_type": "open_ai",
"api_base": "https://api.openai.com/v1",
}

load_dotenv('keys.env')

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_username = os.getenv("REDIS_USER")
redis_password = os.getenv("REDIS_PASS")

long_term_memory = LongTermMemory(redis_host, redis_port, redis_username, redis_password)

class Juliebot:

    def __init__(self, long_term_memory):
        self.long_term_memory = long_term_memory
        self.current_user_data = {'conversation_history': []}
        self.julie_description = julie_description
        

    def start_conversation(self, username):
        history = self.long_term_memory.get_conversation_history(username)
        self.current_user_data = {
        'conversation_history': history if history else []
        }

    def generate_response(self, username, input_text):
        # Start the conversation to access current user data
        self.start_conversation(username)

        # Ensure input_text is a string
        if not isinstance(input_text, str):
            logger.error(f"Expected input_text to be a string, got {type(input_text)}")
            raise ValueError(f"Expected input_text to be a string, got {type(input_text)}")

        # Generate a prompt
        prompt = self.get_prompt(username, input_text)
        logger.error(f"Generated prompt: {prompt}")

        # Generate a response using the chatbot_logic method
        response = self.chatbot_logic(prompt)
            # Ensure response is a string
        if not isinstance(response, str):
            logger.error(f"Expected response to be a string, got {type(response)}")
            raise ValueError(f"Expected response to be a string, got {type(response)}")
        # Vectorize and store the user input and response
        user_input_vector = self.long_term_memory.vectorize_text(input_text)
        response_vector = self.long_term_memory.vectorize_text(response)
        # Log the type of the vectors
        logger.error(f"Type of user_input_vector: {type(user_input_vector)}")
        logger.error(f"Type of response_vector: {type(response_vector)}")
        # Store the vectors in Redis
        self.long_term_memory.store_vector(f"{username}_input", user_input_vector)
        self.long_term_memory.store_vector(f"{username}_response", response_vector)
        # Return the response
        return response

    def get_prompt(self, username, user_input, context=None):
        logger.error(f"get_prompt called with username: '{username}', user_input: '{user_input}', context: '{context}'")

        # Retrieve and format the personalized description for the user
        formatted_julie_description = self.julie_description.format_description(username)
        personalized_description = formatted_julie_description

        # Use the current conversation history retrieved from Redis
        history = self.current_user_data['conversation_history']

        # Build the prompt with the conversation history
        prompt_history = ""
        for entry in history:
            speaker_label = "Human" if entry['role'] == 'user' else "Julie"
            prompt_history += f"{speaker_label}: {entry['content']}\n"

        # Assemble the complete prompt
        prompt = f"The following is a conversation with Julie, a personal assistant. {personalized_description}\n{prompt_history}"
        prompt += f"Human: {user_input}"
        if context:
            prompt += f"\nContext: {context}"
        prompt += "\n\nJulie: "

        logger.error(f"Constructed prompt: '{prompt}'")
        return prompt if prompt else " "


    def chatbot_logic(self, user_inputs, context=None, username='User'):
        # Enhanced logging
        logger.error(f"chatbot_logic called with user_inputs: {user_inputs}, context: {context}, username: {username}")

        # Check for None or invalid input types
        if user_inputs is None:
            logger.error("Received None as user_inputs.")
            return "I'm sorry, but your input was not received. Please try again."
        if not isinstance(user_inputs, (list, str)):
            logger.error(f"Invalid input type: {type(user_inputs)}. Expected a string or a list of strings.")
            return "I'm sorry, but there was an error understanding your input."

        # Handling a single string input
        if isinstance(user_inputs, str):
            user_inputs = [user_inputs]  # Convert single string input to a list

        responses = []
        for user_input in user_inputs:
            try:
                prompt = self.get_prompt(username, user_input, context)
                # Process each input independently
                response = autogen.ChatCompletion.create(prompt=prompt, **autogen_config)
                logger.error(f"Request to autogen: {prompt}")
                responses.append(autogen.ChatCompletion.extract_text(response)[0])
            except Exception as e:
                error_msg = f"An error occurred while processing input '{user_input}': {e}"
                logger.error(error_msg)
                responses.append("I'm sorry, but there was an error processing your request. Please try again later.")

        # Combine responses into a coherent output
        return self.combine_responses(responses, user_inputs)


    def combine_responses(self, responses, user_inputs):

        # This method intelligently combines the individual task responses
        # into a single, coherent message to the user.
        # Initialize a combined response string
        combined_response = ""
        # Iterate over the responses and user inputs together
        for user_input, response in zip(user_inputs, responses):
        # Check if the response is an error message
            if "An error occurred" in response:
                # Log the error with the associated input for debugging
                logger.error(f"Error with input '{user_input}': {response}")
                # Append a user-friendly error message
                combined_response += f"Regarding your request '{user_input}', I encountered an issue. Let's try that part again.\n"
            else:
                # Append the successful response
                combined_response += f"{response}\n"
                # Post-process the combined response if necessary (e.g., removing extra newlines)
                combined_response = self.post_process_combined_response(combined_response)
                return combined_response


    def post_process_combined_response(self, combined_response):

        # This method post-processes the combined response for better readability.
        # For example, it can remove extra whitespace, ensure proper punctuation, etc.
        # Remove any trailing newlines
        combined_response = combined_response.strip()
        # Ensure that the response ends with a period if it doesn't already
        if not combined_response.endswith(('.', '?', '!')):
            combined_response += '.'
        return combined_response
