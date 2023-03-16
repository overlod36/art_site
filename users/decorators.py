from django.shortcuts import redirect, render

def check_profile_activation(view_function):
    def wrapper_function(request, *args, **kwargs):
        if hasattr(request.user, 'student_profile') or hasattr(request.user, 'teacher_profile') or hasattr(request.user, 'admin_profile'):
            return view_function(request, *args, **kwargs)
        else:
            return render(request, 'base_app/error.html', {'error': 'Ваша учетная запись не активирована!'})
    return wrapper_function
