from django.shortcuts import render
from django.urls import reverse
from . models import Course_Announce
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from users.models import Teacher_Profile
from django.http import HttpResponse

def announces(request):
    announces = Course_Announce.objects.all()
    context = { 'announces': announces }
    return render(request, 'informing/announces.html', context)

class CourseAnnounceCreateView(LoginRequiredMixin, CreateView):
    model = Course_Announce
    template_name = 'informing/announce_create.html'
    fields = ['title', 'text', 'course']

    def get_success_url(self):
        return reverse('announces')

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not request.user.groups.all().first().name == 'Teachers':
            return HttpResponse(status=400)
        else:
            return super(CourseAnnounceCreateView, self).dispatch(request)

    def form_valid(self, form):
        # проверка (до перехода по url)
        form.instance.author = Teacher_Profile.objects.filter(user=self.request.user).first()
        return super().form_valid(form)