import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Retrieve all properties from cache or database.
    Uses low-level caching API to cache queryset for 1 hour.
    """
    cache_key = "all_properties"

    # Try to get from cache
    properties = cache.get(cache_key)

    if properties is None:
        # Cache miss - query database
        properties = list(Property.objects.all())
        # Cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)
        logger.info(f"Cache miss: Loaded {len(properties)} properties from database")
    else:
        logger.info(f"Cache hit: Loaded {len(properties)} properties from cache")

    return properties


def get_redis_cache_metrics():
    """
    Retrieve and log Redis cache hit/miss statistics.
    Returns a dictionary with cache metrics.
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")

        # Get Redis info
        info = redis_conn.info("stats")

        # Extract keyspace hits and misses
        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0

        metrics = {
            "keyspace_hits": keyspace_hits,
            "keyspace_misses": keyspace_misses,
            "total_requests": total_requests,
            "hit_ratio": round(hit_ratio, 2),
        }

        # Log metrics
        logger.info(
            f"Redis Cache Metrics - Hits: {keyspace_hits}, Misses: {keyspace_misses}, "
            f"Hit Ratio: {hit_ratio:.2f}%"
        )

        return metrics
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "total_requests": 0,
            "hit_ratio": 0,
            "error": str(e),
        }
