from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def check_teacher_profile(user: User):
    if hasattr(user, 'teacher_profile'): return True
    return False