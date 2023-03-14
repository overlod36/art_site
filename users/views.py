from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student_Profile, Teacher_Profile, Admin_Profile
from educational_app.models import Course
from .decorators import check_profile_activation

@login_required(login_url='/login/')
@check_profile_activation
def profile(request):
    if hasattr(request.user, 'student_profile'):
        profile = Student_Profile.objects.filter(user=request.user).first()
        context = { 'profile' : profile , 
                   'courses': Course.objects.filter(groups = Student_Profile.objects.filter(user=request.user).first().group) }
    elif hasattr(request.user, 'teacher_profile'):
        profile = Teacher_Profile.objects.filter(user=request.user).first()
        context = { 'profile': profile ,
                   'courses': Course.objects.filter(author = Teacher_Profile.objects.filter(user=request.user).first())}
    elif hasattr(request.user, 'admin_profile'):
        profile = Admin_Profile.objects.filter(user=request.user).first()
        context = { 'profile': profile }
    return render(request, 'users/profile.html', context)

