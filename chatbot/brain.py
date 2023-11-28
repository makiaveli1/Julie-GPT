import json
import logging
import redis
from jsonschema import validate
from django.conf import settings

logger = logging.getLogger(__name__)


class LongTermMemory:
    """
    Represents the long-term memory component of the chatbot.

    This class is responsible for managing the conversation history
    and user data using Redis as the storage backend.

    Attributes:
        redis_config (dict): Configuration settings for Redis.
        redis_client (redis.Redis): Redis client for interacting
        with Redis server.
        schema (dict): JSON schema for validating user data.

    Methods:
        __init__(self, config): Initializes the LongTermMemory instance.
        initialize_redis(self): Initializes the Redis client.
        create_redis_client(self): Creates a Redis client with
        connection pooling.
        test_connection(self): Tests the connection to the Redis server.
        get_conversation_history(self, username): Retrieves the conversation
        history for a given username.
        set_user_data(self, username, user_data): Sets the user data for
        a given username.
        update_conversation_history(self, username, role, content):
        Updates the conversation history for a given username.
    """
    def __init__(self, config):
        """
        Initializes the Brain object.

        Args:
            config (dict): Configuration dictionary
            containing Redis settings.

        Returns:
            None
        """
        # Configuration is pulled from Django's settings
        self.redis_config = {
            'HOST': settings.REDIS_HOST,
            'PORT': settings.REDIS_PORT,
            'USERNAME': settings.REDIS_USER,
            'PASSWORD': settings.REDIS_PASS
        }
        self.initialize_redis()
        self.schema = {
            "type": "object",
            "properties": {"conversation_history": {"type": "array"}},
        }

    def initialize_redis(self):
        """
        Initializes the Redis client with connection pooling.
        """
        self.redis_client = self.create_redis_client()
        self.test_connection()

    def create_redis_client(self):
        """
        Create a Redis client using connection pooling.

        Returns:
            redis.Redis: Redis client object.
        """
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
        """
        Test the connection to Redis.

        This method tries to ping the Redis server to check
        if the connection is successful.
        If the connection fails, it raises an appropriate exception.

        Raises:
            redis.ConnectionError: If the connection to Redis fails.
            redis.exceptions.AuthenticationError:
            If the authentication with Redis fails.
            Exception: If any other error occurs during the connection attempt.
        """
        try:
            self.redis_client.ping()
            logger.info(f"""Successfully connected to Redis at
                        {self.redis_config['HOST']}:{
                            self.redis_config['PORT']}.""")
        except redis.ConnectionError as e:
            logger.error("Could not connect to Redis. Connection failed.")
            raise e
        except redis.exceptions.AuthenticationError as e:
            logger.error("""Authentication failed:
                         invalid username-password pair.""")
            raise e
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e

    def get_conversation_history(self, username):
        """
        Retrieve the conversation history for a given username.

        Args:
            username (str): The username for which to
            retrieve the conversation history.

        Returns:
            list: A list of dictionaries representing the conversation history,
            with each dictionary containing the message details.

        Raises:
            Exception: If there is an error
            retrieving the conversation history.
        """
        key = f"chat:{username}"
        try:
            messages = self.redis_client.lrange(key, 0, -1)
            history = [json.loads(m) for m in messages][::-1]
            return history
        except redis.exceptions.RedisError as e:
            error_msg = f"""Failed to retrieve conversation history for
            {username} due to Redis error: {e}"""
            logger.error(error_msg)
            raise Exception(error_msg) from e
        except json.JSONDecodeError as e:
            error_msg = f"""Failed to decode conversation history for
            {username}. Invalid JSON format: {e}"""
            logger.error(error_msg)
            raise Exception(error_msg) from e
        except Exception as e:
            error_msg = f"""An unexpected error occurred while retrieving
            conversation history for {username}: {e}"""
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def set_user_data(self, username, user_data):
        """
        Sets the user data for a given username.

        Args:
            username (str): The username of the user.
            user_data (dict): The user data to be set.

        Raises:
            redis.exceptions.RedisError: If the Redis operation fails.
            Exception: If there is an error validating or saving the user data.

        """
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
        """
        Update the conversation history for a given user.

        Args:
            username (str): The username of the user.
            role (str): The role of the message (e.g., 'user', 'bot').
            content (str): The content of the message.

        Raises:
            redis.exceptions.RedisError: If a Redis operation fails.
            Exception: If there is a general error while
            updating the conversation history.

        """
        key = f"chat:{username}"
        value = json.dumps({"role": role, "content": content})
        try:
            self.redis_client.lpush(key, value)
            logger.info(f"""Added message to conversation history for
                        {username}""")
            # Trimming the list to maintain manageable size
            self.redis_client.ltrim(key, 0, 5000)
            logger.info(f"Trimmed conversation history for {username}")
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis operation failed for {username}")
            raise e
        except Exception as e:
            logger.error(f"""Failed to update conversation
                         history for {username}: {e}""")
            raise e
