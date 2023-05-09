from typing import Any
from django.db.models.query import QuerySet
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from gallery_app.models import Student_Gallery, Student_Picture, Teacher_Picture, Public_Gallery, Public_Picture
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormView
from .forms import StudentGalleryStatusForm, PublicGalleryFilesForm, PublicGalleryInfoForm
from django.db.models import Q
from django.core.paginator import Paginator

class StudentGalleryListView(LoginRequiredMixin, ListView):
    model = Student_Gallery
    template_name = 'gallery/student_galleries_list.html'
    context_object_name = 'st_galleries'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        return Student_Gallery.objects.filter(Q(status='INNER') | Q(status='PUBLIC')).order_by('student__last_name')

class StudentPictureCreateView(LoginRequiredMixin, CreateView):
    model = Student_Picture
    template_name = 'gallery/picture_upload.html'
    fields = ['student_img', 'description']

    def get_form(self, form_class=None):
        if form_class is None: form_class = self.get_form_class()

        form = super(StudentPictureCreateView, self).get_form(form_class)
        form.fields['student_img'].widget.attrs['class'] = 'form-control mb-4'
        form.fields['description'].widget.attrs['placeholder'] = 'Описание картины'
        form.fields['description'].widget.attrs['class'] = 'form-control mb-4'
        form.fields['description'].label = ''
        form.fields['student_img'].label = ''
        return form

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

class StudentPictureDeleteView(LoginRequiredMixin, DeleteView):
    model = Student_Picture
    template_name = 'gallery/picture_delete.html'

    def get_success_url(self):
        return reverse('main')
    
class PublicGalleryUpdateView(LoginRequiredMixin, UpdateView):
    model = Public_Gallery
    template_name = 'gallery/gallery_update.html'
    fields = ['title', 'description']

    def get_form(self, form_class=None):
        if form_class is None: form_class = self.get_form_class()

        form = super(PublicGalleryUpdateView, self).get_form(form_class)
        form.fields['title'].widget.attrs['class'] = 'form-control mb-4'
        form.fields['title'].widget.attrs['placeholder'] = 'Название галереи'
        form.fields['description'].widget=forms.Textarea(attrs={'placeholder': 'Описание галереи', "rows":"8"})
        form.fields['description'].widget.attrs['class'] = 'form-control mb-4'
        form.fields['description'].label = ''
        form.fields['title'].label = ''
        return form

    def get_success_url(self) -> str:
        return reverse('profile')

class PublicGalleryDeleteView(LoginRequiredMixin, DeleteView):
    model = Public_Gallery
    template_name = 'gallery/gallery_delete.html'

    def get_success_url(self) -> str:
        return reverse('profile')

@login_required(login_url='/login/')
def get_student_gallery(request, id):
    page = request.GET.get('page', 1)
    gallery = Student_Gallery.objects.get(pk=id)
    images = Student_Picture.objects.filter(student_gallery=gallery).order_by('publish_date') 
    form = StudentGalleryStatusForm(initial={'status': gallery.status})
    paginator = Paginator(images, per_page=4)
    content = paginator.get_page(page)
    # page_object = paginator.get_page(page)
    context = {'content': content, 'images': images, 'gallery': gallery}
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

@login_required(login_url="/login/")
def get_public_gallery(request, id):
    page = request.GET.get('page', 1)
    gal = Public_Gallery.objects.get(pk=id)
    images = Public_Picture.objects.filter(public_gallery=gal).order_by('publish_date')
    paginator = Paginator(images, per_page=4)
    content = paginator.get_page(page)
    context = {'content': content, 'images': images, 'gallery': gal}
    template = 'gallery/public_gallery.html'
    return render(request, template, context)

@login_required(login_url='/login/')
def create_public_gallery(request):
    info_form = PublicGalleryInfoForm()
    file_form = PublicGalleryFilesForm()

    if request.method == 'POST':
        pub_gal = Public_Gallery(title=request.POST['title'], 
                                 description=request.POST['description'],
                                 author=request.user.teacher_profile)
        pub_gal.save()
        if request.FILES:
            for file in request.FILES.getlist('files'):
                pic = Public_Picture(public_img=file, public_gallery=pub_gal)
                pic.save()
        return redirect('profile')

    return render(request, 'gallery/public_gallery_create.html', context={'info_form': info_form, 'file_form': file_form})

@login_required(login_url='/login/')
def load_public_picture(request, id):
    file_form = PublicGalleryFilesForm()
    if request.method == 'POST':
        if request.FILES:
            for file in request.FILES.getlist('files'):
                pic = Public_Picture(public_img=file, public_gallery=Public_Gallery.objects.get(pk=id))
                pic.save()
        return redirect('main')
    return render(request, 'gallery/public_picture_load.html', context={'file_form': file_form})