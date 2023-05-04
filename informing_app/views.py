from django.shortcuts import render, redirect
from django.urls import reverse
from . models import Course_Announce
from educational_app.models import Course
from .forms import OneCourseAnnounceForm, CourseAnnounceForm, NewsAnnounceForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.decorators import check_profile_activation

@login_required(login_url='/login/')
@check_profile_activation
def announces(request):
    if hasattr(request.user, 'student_profile'):
        group = request.user.student_profile.group
        context = { 'announces': Course_Announce.objects.filter(course__in=Course.objects.filter(groups=group).all()).order_by('-publish_date') }
    elif hasattr(request.user, 'teacher_profile'):
        context = { 'announces': Course_Announce.objects.filter(course__in=Course.objects.filter(author=request.user.teacher_profile).all()).order_by('-publish_date') }
    elif hasattr(request.user, 'admin_profile'):
        announces = Course_Announce.objects.all().order_by('-publish_date')
        context = { 'announces': announces }
    return render(request, 'informing/announces.html', context)

def delete_announce(request, id):
    announce = Course_Announce.objects.get(pk=id)
    if request.method == 'POST':
        announce.delete()
        return redirect('main')
    context = { 'item': announce , 'name': 'объявление' }
    return render(request, 'informing/announce_delete.html', context)

class OneCourseAnnounceCreateView(LoginRequiredMixin, CreateView):
    form_class = OneCourseAnnounceForm
    template_name = 'informing/announce_create.html'

    def get_success_url(self):
        return reverse('announces')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['pk']
            return super(OneCourseAnnounceCreateView, self).dispatch(request)

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.pk)
        return super().form_valid(form)

class CourseAnnounceCreateView(LoginRequiredMixin, CreateView):
    form_class = CourseAnnounceForm
    template_name = 'informing/announce_create.html'

    def get_success_url(self):
        return reverse('announces')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            return super(CourseAnnounceCreateView, self).dispatch(request)

    def get_form_kwargs(self):
        kwargs = super(CourseAnnounceCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

class NewsAnnounceCreateView(LoginRequiredMixin, CreateView):
    form_class = NewsAnnounceForm
    template_name = 'informing/news_create.html'

    def get_success_url(self):
        return reverse('main')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'teacher_profile'):
            return HttpResponse(status=400)
        else:
            self.user = request.user.teacher_profile
            return super(NewsAnnounceCreateView, self).dispatch(request)

    def form_valid(self, form):
        form.instance.author = self.user
        return super().form_valid(form)

def news_announce_create(request):
    return render(request, 'informing/news_create.html')