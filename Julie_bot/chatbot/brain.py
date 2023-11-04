
from sentence_transformers import SentenceTransformer
import numpy as np
import redis
import json
import logging
from jsonschema import validate, ValidationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class LongTermMemory:
    """
    A singleton class that represents the long-term memory of the chatbot.
    It uses Redis as the storage backend.
    """

    def __init__(self, host, port, username, password):
        self.redis_host = host
        self.redis_port = port
        self.redis_username = username
        self.redis_password = password
        self.initialize_redis()
        self.schema = {
            "type": "object",
            "properties": {"conversation_history": {"type": "array"}},
        }

    def initialize_redis(self):
        """
        Initialize the Redis client and test the connection.
        """
        self.redis_client = self.create_redis_client()
        self.test_connection()

    def create_redis_client(self):
        return redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            username=self.redis_username,
            password=self.redis_password,
            decode_responses=True,
            socket_timeout=60,
        )

    def test_connection(self):
        try:
            self.redis_client.ping()
            logging.info(
                f"Successfully connected to Redis at {self.redis_host}:{self.redis_port}."
            )
        except redis.ConnectionError as e:
            logging.error("Could not connect to Redis. Connection failed.")
            raise e
        except redis.exceptions.AuthenticationError as e:
            logging.error(
                "Authentication failed: invalid username-password pair."
            )
            raise e
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")
            raise e

    def vectorize_text(self, text):
        """
        Convert text to vector using a machine learning model.
        """
        model = SentenceTransformer('msmarco-distilbert-base-v4')  # Example model

        if isinstance(text, str):
            text = [text]  # Convert single string to a list

        if not all(isinstance(t, str) for t in text):
            logging.error(f"vectorize_text received invalid input: {text}")
            raise ValueError("Input text must be a string or a list of strings.")

        return model.encode(text)

    def store_vector(self, username, vector):
        if not isinstance(vector, (np.ndarray, list)):
            logging.error(f"Expected vector to be a numpy array or a list, got {type(vector)}")
            raise ValueError(f"Expected vector to be a numpy array or a list, got {type(vector)}")

        vector_list = vector if isinstance(vector, list) else vector.tolist()

        key = f"vec:{username}"
        try:
            self.redis_client.execute_command('HSET', key, 'vector', json.dumps(vector_list))
            logging.info(f"Stored vector for {username}")
        except Exception as e:
            logging.error(f"Failed to store vector for {username}: {e}")
            raise e

    def search_similar_conversations(self, username, text):
        vector = self.vectorize_text(text)

        vector_list = vector.tolist() if isinstance(vector, np.ndarray) else vector

        try:
            results = self.redis_client.execute_command('FT.SEARCH', f'idx:{username}', f'@vector:[{",".join(map(str, vector_list))}]')
            logging.info(f"Search results: {results}")
            return results
        except Exception as e:
            logging.error(f"Failed to search for similar conversations for {username}: {e}")
            raise e

    def update_conversation_history_with_vector(self, username, role, content):
        vector = self.vectorize_text(content)
        self.store_vector(username, vector)
        self.update_conversation_history(username, role, content)

    def get_conversation_history(self, username):
        key = f"chat:{username}"
        try:
            messages = self.redis_client.lrange(key, 0, -1)
            history = [json.loads(m) for m in messages][::-1]
            return history
        except redis.exceptions.RedisError as e:
            error_msg = f"Failed to retrieve conversation history for {username} due to Redis error: {e}"
            logging.error(error_msg)
            raise Exception(error_msg) from e
        except json.JSONDecodeError as e:
            error_msg = f"Failed to decode conversation history for {username}. Invalid JSON format: {e}"
            logging.error(error_msg)
            raise Exception(error_msg) from e
        except Exception as e:
            error_msg = f"An unexpected error occurred while retrieving conversation history for {username}: {e}"
            logging.error(error_msg)
            raise Exception(error_msg) from e

    def set_user_data(self, username, user_data):
        try:
            validate(instance=user_data, schema=self.schema)
            self.redis_client.set(username, json.dumps(user_data))
            logging.info(f"Saved user data for {username}")
        except redis.exceptions.RedisError as e:
            logging.error(f"Redis operation failed for {username}")
            raise e
        except Exception as e:
            logging.error(f"Failed to load user data for {username}: {e}")
            raise e

    def update_conversation_history(self, username, role, content):
        key = f"chat:{username}"
        value = json.dumps({"role": role, "content": content})
        try:
            self.redis_client.lpush(key, value)
            logging.info(
                f"Added message to conversation history for {username}"
            )

            self.redis_client.ltrim(key, 0, 5000)
            logging.info(f"Trimmed conversation history for {username}")
        except redis.exceptions.RedisError as e:
            logging.error(f"Redis operation failed for {username}")
            raise e
        except Exception as e:
            logging.error(
                f"Failed to update conversation history for {username}: {e}"
            )
            raise e
