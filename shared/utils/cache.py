from typing import Any, Optional
from functools import wraps
import time
import json
from datetime import datetime
import redis
from shared.utils.logger import cv_logger

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.redis = redis.Redis(host=host, port=port, db=db)
            self.redis.ping()
            cv_logger.info("Redis cache initialized successfully")
        except redis.ConnectionError:
            cv_logger.warning("Redis not available, falling back to in-memory cache")
            self.redis = None
            self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            if self.redis:
                value = self.redis.get(key)
                return json.loads(value) if value else None
            return self._cache.get(key, {}).get('value')
        except Exception as e:
            cv_logger.error(f"Error getting from cache: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL in seconds."""
        try:
            if self.redis:
                return self.redis.setex(
                    key,
                    ttl,
                    json.dumps(value)
                )
            self._cache[key] = {
                'value': value,
                'expires': time.time() + ttl
            }
            return True
        except Exception as e:
            cv_logger.error(f"Error setting cache: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            if self.redis:
                return bool(self.redis.delete(key))
            return bool(self._cache.pop(key, None))
        except Exception as e:
            cv_logger.error(f"Error deleting from cache: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache."""
        try:
            if self.redis:
                return self.redis.flushdb()
            self._cache.clear()
            return True
        except Exception as e:
            cv_logger.error(f"Error clearing cache: {str(e)}")
            return False

# Cache decorator
def cached(ttl: int = 3600):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds (default: 1 hour)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                cv_logger.debug(f"Cache hit for {key}")
                return result
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(key, result, ttl)
            cv_logger.debug(f"Cache miss for {key}, stored result")
            
            return result
        return wrapper
    return decorator

# Initialize global cache instance
cache = Cache() 