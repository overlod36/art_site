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

    # def form_valid(self, form):
    #     return super().form_valid(form)