
from redis import Redis
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class LongTermMemory:
    def __init__(self):
        # Configuration is now pulled from Django's settings
        self.redis_config = {
            'HOST': settings.REDIS_HOST,
            'PORT': settings.REDIS_PORT,
            'USERNAME': settings.REDIS_USER,
            'PASSWORD': settings.REDIS_PASS
        }
        self.initialize_redis()

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

    def update_conversation_history(self, user_name, role, message):
        # Storing conversation history in Redis without vectorization
        history_key = f"conversation_history:{user_name}"
        history = self.redis_client.get(history_key)
        if history:
            history = json.loads(history)
        else:
            history = []

        history.append({"role": role, "message": message})
        self.redis_client.set(history_key, json.dumps(history))
