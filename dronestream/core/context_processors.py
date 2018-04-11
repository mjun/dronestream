from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def google_maps_api_key(request):
    try:
        return {'GOOGLE_MAPS_API_KEY': getattr(settings, "GOOGLE_MAPS_API_KEY")}
    except AttributeError:
        raise ImproperlyConfigured("GOOGLE_MAPS_API_KEY setting not specified.")
