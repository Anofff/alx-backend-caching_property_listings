import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate cache when a property is created or updated.
    """
    cache_key = "all_properties"
    cache.delete(cache_key)
    logger.info(f"Cache invalidated: Property '{instance.title}' was saved")


@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate cache when a property is deleted.
    """
    cache_key = "all_properties"
    cache.delete(cache_key)
    logger.info(f"Cache invalidated: Property '{instance.title}' was deleted")
