from django.shortcuts import redirect, render

def check_profile_activation(view_function):
    def wrapper_function(request, *args, **kwargs):
        # if not request.user.groups.filter(name__in=['Students', 'Teachers', 'Admins']).exists():
        #     return render(request, 'users/error_profile.html', {'error': 'Ваша учетная запись не активирована!'})
        if hasattr(request.user, 'student_profile') or hasattr(request.user, 'teacher_profile') or hasattr(request.user, 'admin_profile'):
            return view_function(request, *args, **kwargs)
        else:
            return render(request, 'users/error_profile.html', {'error': 'Ваша учетная запись не активирована!'})
    return wrapper_function
