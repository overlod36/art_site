from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='format')
def date_format(date: datetime):
    # if date == None: return 'Без посещений'
    return date.strftime("%d.%m.%Y %H:%M")