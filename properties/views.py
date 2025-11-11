from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties, get_redis_cache_metrics


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties as JSON.
    Cached for 15 minutes using cache_page decorator.
    """
    properties = get_all_properties()
    # Log cache metrics when viewing properties
    get_redis_cache_metrics()

    # Serialize properties to JSON
    properties_data = [
        {
            "id": prop.id,
            "title": prop.title,
            "description": prop.description,
            "price": str(prop.price),
            "location": prop.location,
            "created_at": prop.created_at.isoformat(),
        }
        for prop in properties
    ]

    return JsonResponse({"properties": properties_data}, safe=False)


def cache_metrics(request):
    """
    View to display Redis cache metrics as JSON.
    """
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)
