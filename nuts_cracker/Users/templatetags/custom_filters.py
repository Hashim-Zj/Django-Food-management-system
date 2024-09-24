import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def file_exists(file_url):
    if file_url:
        file_path = os.path.join(settings.MEDIA_ROOT, 'products', os.path.basename(file_url))
        return os.path.isfile(file_path)
    return False