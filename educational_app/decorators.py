from django.shortcuts import redirect, render
from .models import Course

def check_course_existence(view_function):
    def wrapper_function(request, *args, **kwargs):
        if Course.objects.filter(pk=kwargs['id']).exists():
            return view_function(request, *args, **kwargs)
        return render(request, 'base_app/error.html', {'error': 'Такого курса нет!'})
    return wrapper_function