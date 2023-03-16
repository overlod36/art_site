from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from users.models import Teacher_Profile
from .decorators import check_course_existence

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'educational/course_create.html'
    fields = ['title', 'groups', 'description']

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            return super(CourseCreateView, self).dispatch(request)

    def form_valid(self, form):
        # проверка (до перехода по url)
        form.instance.author = self.request.user.teacher_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')

@login_required(login_url='/login/')
@check_course_existence
def get_course(request, id):
    return render(request, 'educational/course.html', {'course': Course.objects.filter(pk=id).first()})


