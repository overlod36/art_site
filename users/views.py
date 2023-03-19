from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from educational_app.models import Course
from .decorators import check_profile_activation
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StudentForm
from django.urls import reverse

@login_required(login_url='/login/')
@check_profile_activation
def profile(request):
    if hasattr(request.user, 'student_profile'):
        context = { 'profile' : request.user.student_profile , 
                   'courses': Course.objects.filter(groups = request.user.student_profile.group) }
    elif hasattr(request.user, 'teacher_profile'):
        context = { 'profile': request.user.teacher_profile ,
                   'courses': Course.objects.filter(author = request.user.teacher_profile)}
    elif hasattr(request.user, 'admin_profile'):
        context = { 'profile': request.user.admin_profile }
    return render(request, 'users/profile.html', context)

class StudentCreateView(LoginRequiredMixin, CreateView):
    form_class = StudentForm
    template_name = 'users/student_create.html'

    def get_success_url(self):
        return reverse('announces')

    def form_valid(self, form):
        user = form['user'].save()
        profile = form['student'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.get_success_url())

