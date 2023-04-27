from django.forms import Form, ModelForm
from gallery_app.models import Student_Gallery
from django import forms

class StudentGalleryStatusForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentGalleryStatusForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
        
    class Meta:
        model = Student_Gallery
        fields = ['status']
