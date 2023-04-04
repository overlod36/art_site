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
from .models import Course, Lecture, Test
from informing_app.models import Course_Announce
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from users.models import Teacher_Profile
from .decorators import check_course_existence, course_access, check_test_existence
from django.http import HttpRequest
import json

class LectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    template_name = 'educational/lecture_create.html'
    fields = ['file']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        if Course.objects.get(pk=kwargs['id']).author != request.user.teacher_profile:
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['id']
            return super(LectureCreateView, self).dispatch(request)
    
    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')

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
        form.instance.author = self.request.user.teacher_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')

@login_required(login_url='/login/')
@check_course_existence
@course_access
def get_course(request, id):
    f_course = Course.objects.filter(pk=id).first()
    return render(request, 'educational/course.html', 
                  {'course': f_course, 
                   'lectures': Lecture.objects.filter(course=f_course).all(),
                   'announces': Course_Announce.objects.filter(course=f_course).order_by('-publish_date'),
                   'tests': Test.objects.filter(course=f_course).all()})

@login_required(login_url='/login/')
@check_test_existence
def get_test(request, id):
    test = Test.objects.get(pk=id)
    with open(test.filepath, encoding='utf-8') as json_file:
        test_f = json.load(json_file)
    return render(request, 'educational/test.html', {'test': test_f})

def get_lecture(request, id):
    lecture = Lecture.objects.get(pk=id)
    resp = HttpResponse(lecture.file, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{ lecture.filename }"'
    return resp


