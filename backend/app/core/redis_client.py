import redis
from app.core.config import settings

# Redis client for short-term memory and cache
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    encoding="utf-8"
)


def get_redis():
    """Get Redis client instance"""
    return redis_client
