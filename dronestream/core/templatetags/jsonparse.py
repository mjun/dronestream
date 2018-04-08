import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()


@register.filter(name='json')
def queryset_to_json(queryset):
    return json.dumps(list(queryset), cls=DjangoJSONEncoder)
