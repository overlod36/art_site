from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from gallery_app.models import Student_Gallery, Student_Picture, Teacher_Picture
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import StudentGalleryStatusForm
from django.db.models import Q

class StudentGalleryListView(LoginRequiredMixin, ListView):
    model = Student_Gallery
    template_name = 'gallery/student_galleries_list.html'
    context_object_name = 'st_galleries'

    def get_queryset(self) -> QuerySet[Any]:
        return Student_Gallery.objects.filter(Q(status='INNER') | Q(status='PUBLIC'))

class StudentPictureCreateView(LoginRequiredMixin, CreateView):
    model = Student_Picture
    template_name = 'gallery/picture_upload.html'
    fields = ['student_img', 'description']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'student_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['id']
            return super(StudentPictureCreateView, self).dispatch(request)

    def form_valid(self, form):
        form.instance.student_gallery = Student_Gallery.objects.get(pk=self.pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')

@login_required(login_url='/login/')
def get_student_gallery(request, id):
    # первичная проверка на студента (нужно для отображения формы)
    gallery = Student_Gallery.objects.get(pk=id)
    images = Student_Picture.objects.filter(student_gallery=gallery) 
    form = StudentGalleryStatusForm(initial={'status': gallery.status})
    context = {'gallery': gallery, 'images': images}
    template = 'gallery/student_gallery.html'
    if hasattr(request.user, 'student_profile'):
        if request.user.student_profile == gallery.student:
            context['form'] = form
            template = 'gallery/own_student_gallery.html'
        
    if request.method == 'POST':
        # доп проверка?
        gallery.status = request.POST['status']
        gallery.save()
        return redirect('student-gallery', id=gallery.pk)

    return render(request, template, context)