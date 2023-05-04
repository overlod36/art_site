from .models import Course_Announce, News_Announce
from django import forms 
from users.models import Teacher_Profile
from educational_app.models import Course
from django_ckeditor_5.widgets import CKEditor5Widget

class OneCourseAnnounceForm(forms.ModelForm):
    class Meta:
        model = Course_Announce
        fields = ['title', 'text']
    
class CourseAnnounceForm(forms.ModelForm):
    class Meta:
        model = Course_Announce
        fields = ['title', 'text', 'course']
    
    def __init__(self, *args, **kwargs):
        to_user = kwargs.pop('user')
        super(CourseAnnounceForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(author=to_user.teacher_profile).all()

class NewsAnnounceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["html"].required = False

    class Meta:
        model = News_Announce
        fields = ['title', 'html']
        widgets = {'html': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              )}