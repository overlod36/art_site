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

class StudentPictureCreateView(LoginRequiredMixin, CreateView):
    model = Student_Picture
    template_name = 'gallery/picture_upload.html'
    fields = ['img', 'description']

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
    gallery = Student_Gallery.objects.get(pk=id)
    images = Student_Picture.objects.filter(student_gallery=gallery) 
    form = StudentGalleryStatusForm(initial={'status': gallery.status})
    if request.method == 'POST':
        gallery.status = request.POST['status']
        gallery.save()
        return redirect('student-gallery', id=gallery.pk)

    return render(request, 'gallery/student_gallery.html', 
                  context={'gallery': gallery, 'images': images, 'form': form})