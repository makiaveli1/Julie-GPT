from sentence_transformers import SentenceTransformer
import numpy as np
import redis
import json
import logging
from jsonschema import validate, ValidationError
from django.conf import settings

logger = logging.getLogger(__name__)

class LongTermMemory:
    def __init__(self, config):
        # Configuration is now pulled from Django's settings
        self.redis_config = {
            'HOST': settings.REDIS_HOST,
            'PORT': settings.REDIS_PORT,
            'USERNAME': settings.REDIS_USER,
            'PASSWORD': settings.REDIS_PASS
        }
        self.initialize_model()
        self.initialize_redis()
        self.schema = {
            "type": "object",
            "properties": {"conversation_history": {"type": "array"}},
        }

    def initialize_model(self):
        # Initialize SentenceTransformer model only once for efficiency
        self.model = SentenceTransformer('msmarco-distilbert-base-v4')

    def initialize_redis(self):
        # Initialize Redis client with connection pooling
        self.redis_client = self.create_redis_client()
        self.test_connection()

    def create_redis_client(self):
        # Using connection pooling for Redis
        pool = redis.ConnectionPool(
            host=self.redis_config['HOST'],
            port=self.redis_config['PORT'],
            username=self.redis_config['USERNAME'],
            password=self.redis_config['PASSWORD'],
            decode_responses=True,
            socket_timeout=60
        )
        return redis.Redis(connection_pool=pool)

    def test_connection(self):
        try:
            self.redis_client.ping()
            logger.info(f"Successfully connected to Redis at {self.redis_config['HOST']}:{self.redis_config['PORT']}.")
        except redis.ConnectionError as e:
            logger.error("Could not connect to Redis. Connection failed.")
            raise e
        except redis.exceptions.AuthenticationError as e:
            logger.error("Authentication failed: invalid username-password pair.")
            raise e
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e

    def vectorize_text(self, text):
        if isinstance(text, str):
            text = [text]
        if not all(isinstance(t, str) for t in text):
            logger.error(f"vectorize_text received invalid input: {text}")
            raise ValueError("Input text must be a string or a list of strings.")
        return self.model.encode(text)

    def store_vector(self, username, vector):
        if not isinstance(vector, (np.ndarray, list)):
            logger.error(f"Expected vector to be a numpy array or a list, got {type(vector)}")
            raise ValueError(f"Expected vector to be a numpy array or a list, got {type(vector)}")
        vector_list = vector if isinstance(vector, list) else vector.tolist()
        key = f"vec:{username}"
        try:
            self.redis_client.hset(key, 'vector', json.dumps(vector_list))
            logger.info(f"Stored vector for {username}")
        except Exception as e:
            logger.error(f"Failed to store vector for {username}: {e}")
            raise e

    def search_similar_conversations(self, username, text):
        vector = self.vectorize_text(text)
        vector_list = vector.tolist() if isinstance(vector, np.ndarray) else vector
        try:
            # Improved search using Redis Search commands
            results = self.redis_client.execute_command('FT.SEARCH', f'idx:{username}', f'@vector:[{",".join(map(str, vector_list))}]')
            logger.info(f"Search results: {results}")
            return results
        except Exception as e:
            logger.error(f"Failed to search for similar conversations for {username}: {e}")
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
            logger.error(error_msg)
            raise Exception(error_msg) from e
        except json.JSONDecodeError as e:
            error_msg = f"Failed to decode conversation history for {username}. Invalid JSON format: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
        except Exception as e:
            error_msg = f"An unexpected error occurred while retrieving conversation history for {username}: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def set_user_data(self, username, user_data):
        try:
            validate(instance=user_data, schema=self.schema)
            self.redis_client.set(username, json.dumps(user_data))
            logger.info(f"Saved user data for {username}")
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis operation failed for {username}")
            raise e
        except Exception as e:
            logger.error(f"Failed to load user data for {username}: {e}")
            raise e

    def update_conversation_history(self, username, role, content):
        key = f"chat:{username}"
        value = json.dumps({"role": role, "content": content})
        try:
            self.redis_client.lpush(key, value)
            logger.info(f"Added message to conversation history for {username}")
            # Trimming the list to maintain manageable size
            self.redis_client.ltrim(key, 0, 5000)
            logger.info(f"Trimmed conversation history for {username}")
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis operation failed for {username}")
            raise e
        except Exception as e:
            logger.error(f"Failed to update conversation history for {username}: {e}")
            raise e
