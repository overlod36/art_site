from .models import Course_Announce
from django.forms import ModelForm
from users.models import Teacher_Profile
from educational_app.models import Course

class ClassAnnounceForm(ModelForm):
    class Meta:
        model = Course_Announce
        fields = ['title', 'text', 'course']
    
    def __init__(self, *args, **kwargs):
        to_user = kwargs.pop('user')
        super(ClassAnnounceForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(author=to_user.teacher_profile).all()