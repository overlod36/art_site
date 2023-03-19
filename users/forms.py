from django import forms
from .models import Teacher_Profile, Student_Profile, Admin_Profile
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {'username': 'Логин', 'password': 'Пароль'}

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student_Profile
        fields = ['first_name', 'last_name', 'sur_name', 'group']

# class TeacherProfileForm(forms.ModelForm):
#     class Meta:
#         model = Teacher_Profile

# class AdminProfileForm(forms.ModelForm):
#     class Meta:
#         model = Admin_Profile

class StudentForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'student': StudentProfileForm
    }

# class TeacherForm(MultiModelForm):
#     form_classes = {
#         'user': UserForm,
#         'teacher': TeacherProfileForm
#     }

# class AdminForm(MultiModelForm):
#     form_classes = {
#         'user': UserForm,
#         'admin': AdminProfileForm
#     }