from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='format')
def date_format(date: datetime):
    return date.strftime("%H:%M %d:%m:%Y")