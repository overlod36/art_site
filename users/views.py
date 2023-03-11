from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student_Profile, Teacher_Profile
from educational_app.models import Course

@login_required(login_url='/login/')
def profile(request):
    # декоратор на проверку наличия профиля
    if Student_Profile.objects.filter(user=request.user):
        profile = Student_Profile.objects.filter(user=request.user).first()
        context = { 'profile' : profile , 
                   'courses': Course.objects.filter(groups = Student_Profile.objects.filter(user=request.user).first().group),
                   'profile_name': profile._meta.object_name }
    elif Teacher_Profile.objects.filter(user=request.user):
        profile = Teacher_Profile.objects.filter(user=request.user).first()
        context = { 'profile': profile ,
                   'courses': Course.objects.filter(author = Teacher_Profile.objects.filter(user=request.user).first()),
                   'profile_name': profile._meta.object_name }
    else:
        pass
    return render(request, 'users/profile.html', context)

