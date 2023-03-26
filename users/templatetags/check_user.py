from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def define_profile(user: User):
    if hasattr(user, 'teacher_profile'): return 'teacher'
    elif hasattr(user, 'student_profile'): return 'student'
    elif hasattr(user, 'admin_profile'): return 'admin'

@register.simple_tag
def return_login(user: User):
    return user.get_username()