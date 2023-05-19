from django import forms
from .models import Teacher_Profile, Student_Profile, Admin_Profile, Study_Group
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm

class StudyGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudyGroupForm, self).__init__(*args, **kwargs)
        self.fields['number'].label = ''
        self.fields['number'].widget.attrs['placeholder'] = 'Номер группы'
        self.fields['number'].widget.attrs['class'] = 'form-control mb-4'
        

    class Meta:
        model = Study_Group
        fields = ['number']

class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Логин'
        self.fields['username'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password'].widget.attrs['class'] = 'form-control mb-4'

    class Meta:
        model = User
        fields = ['username', 'password']

class StudentProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['last_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['sur_name'].label = ''
        self.fields['sur_name'].widget.attrs['placeholder'] = 'Отчество'
        self.fields['sur_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['group'].widget.attrs['class'] = 'form-select'
        self.fields['group'].label = ''

    class Meta:
        model = Student_Profile
        fields = ['first_name', 'last_name', 'sur_name', 'group']

class TeacherProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['last_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['sur_name'].label = ''
        self.fields['sur_name'].widget.attrs['placeholder'] = 'Отчество'
        self.fields['sur_name'].widget.attrs['class'] = 'form-control mb-4'

    class Meta:
        model = Teacher_Profile
        fields = ['first_name', 'last_name', 'sur_name']

class AdminProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['last_name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['sur_name'].label = ''
        self.fields['sur_name'].widget.attrs['placeholder'] = 'Отчество'
        self.fields['sur_name'].widget.attrs['class'] = 'form-control mb-4'

    class Meta:
        model = Admin_Profile
        fields = ['first_name', 'last_name', 'sur_name']

class StudentForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'student': StudentProfileForm
    }

class TeacherForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'teacher': TeacherProfileForm
    }

class AdminForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'admin': AdminProfileForm 
    }