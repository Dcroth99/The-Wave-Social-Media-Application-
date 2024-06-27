# users/templatetags/custom_filters.py
from django import template
from django.urls import reverse
from django.utils.html import format_html
import re

register = template.Library()

@register.filter
def mention_to_link(value):
    def replace_mention(match):
        username = match.group(1)
        url = reverse('profile', kwargs={'username': username})
        return f'<a href="{url}">@{username}</a>'
    
    return format_html(re.sub(r'@(\w+)', replace_mention, value))