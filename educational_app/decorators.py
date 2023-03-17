from django.shortcuts import redirect, render
from .models import Course

def check_course_existence(view_function):
    def wrapper_function(request, *args, **kwargs):
        if Course.objects.filter(pk=kwargs['id']).exists():
            return view_function(request, *args, **kwargs)
        return render(request, 'base_app/error.html', {'error': 'Такого курса нет!'})
    return wrapper_function

def course_access(view_function):
    def wrapper_function(request, *args, **kwargs):
        if hasattr(request.user, 'student_profile') and Course.objects.get(pk=kwargs['id']) in Course.objects.filter(groups=request.user.student_profile.group).all():
            return view_function(request, *args, **kwargs)
        elif hasattr(request.user, 'teacher_profile') and Course.objects.get(pk=kwargs['id']) in Course.objects.filter(author=request.user.teacher_profile).all():
            return view_function(request, *args, **kwargs)
        elif hasattr(request.user, 'admin_profile'):
            return view_function(request, *args, **kwargs)
        return render(request, 'base_app/error.html', {'error': 'Нет доступа к курсу!'})
    return wrapper_function