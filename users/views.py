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
from .forms import StudentForm, TeacherForm, AdminForm, StudyGroupForm, UserForm
from .models import Student_Profile, Teacher_Profile, Admin_Profile
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms import modelform_factory

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

class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/pass_update.html'
    fields = ['password']
    initial = {'password': ''}

    def get_success_url(self):
        return reverse('main')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['pk']
            return super(PasswordUpdateView, self).dispatch(request, *args, **kwargs)
    
    def get_form_class(self):
        return modelform_factory(self.object.__class__, fields=self.fields, labels={'password': 'Пароль'})

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form['password'].value())
        user.save()
        return redirect(self.get_success_url())
    
class LoginUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/log_update.html'
    fields = ['username']

    def get_success_url(self):
        return reverse('main')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            self.pk = kwargs['pk']
            return super(LoginUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return modelform_factory(self.object.__class__, fields=self.fields, labels={'username': 'Логин'})

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

class TeacherCreateView(LoginRequiredMixin, CreateView):
    form_class = TeacherForm
    template_name = 'users/teacher_create.html'

    def get_success_url(self):
        return reverse('main')
    
    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(TeacherCreateView, self).dispatch(request)

    def form_valid(self, form):
        user = form['user'].save(commit=False)
        user.password = make_password(form['user']['password'].value())
        user.save()
        profile = form['teacher'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.get_success_url())

class TeachersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/teachers_list.html'
    context_object_name = 'teachers'

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(TeachersListView, self).dispatch(request)

    def get_queryset(self):
        return User.objects.filter(teacher_profile__id__isnull=False)

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher_Profile
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'sur_name']

    def get_success_url(self):
        return reverse('main')

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

class AdminCreateView(LoginRequiredMixin, CreateView):
    form_class = AdminForm
    template_name = 'users/admin_create.html'

    def get_success_url(self):
        return reverse('main')

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(AdminCreateView, self).dispatch(request)

    def form_valid(self, form):
        user = form['user'].save(commit=False)
        user.is_staff = True
        user.password = make_password(form['user']['password'].value())
        user.save()
        profile = form['admin'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.get_success_url())

class AdminUpdateView(LoginRequiredMixin, UpdateView):
    model = Admin_Profile
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'sur_name']

    def get_success_url(self):
        return reverse('main')

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

class AdminsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/admins_list.html'
    context_object_name = 'admins'

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(AdminsListView, self).dispatch(request)

    def get_queryset(self):
        return User.objects.filter(admin_profile__id__isnull=False)

class StudentsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/students_list.html'
    context_object_name = 'students'

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(StudentsListView, self).dispatch(request)

    def get_queryset(self):
        return User.objects.filter(student_profile__id__isnull=False)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student_Profile
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'sur_name', 'group']

    def get_success_url(self):
        return reverse('main')

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

class StudentCreateView(LoginRequiredMixin, CreateView):
    form_class = StudentForm
    template_name = 'users/student_create.html'

    def get_success_url(self):
        return reverse('main')

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(StudentCreateView, self).dispatch(request)

    def form_valid(self, form):
        user = form['user'].save(commit=False)
        user.password = make_password(form['user']['password'].value())
        user.save()
        profile = form['student'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.get_success_url())

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'

    def get_success_url(self):
        return reverse('main')

class StudyGroupCreateView(LoginRequiredMixin, CreateView):
    form_class = StudyGroupForm
    template_name = 'users/group_create.html'

    def get_success_url(self):
        return reverse('main')

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponse(status=400)
        else:
            return super(StudyGroupCreateView, self).dispatch(request)
    
    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

