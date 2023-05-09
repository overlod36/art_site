from django import forms
from gallery_app.models import Student_Gallery, Public_Gallery
from django import forms
from betterforms.multiform import MultiForm

class StudentGalleryStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentGalleryStatusForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
                field.widget.attrs['class'] = 'form-select'
        
    class Meta:
        model = Student_Gallery
        fields = ['status']
    
class PublicGalleryInfoForm(forms.ModelForm):
    class Meta:
        model = Public_Gallery
        fields = ['title', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['title'].widget.attrs['placeholder'] = 'Название галереи'
        self.fields['title'].label = ''
        self.fields['description'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание галереи'
        self.fields['description'].label = ''


class PublicGalleryFilesForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control mb-4'}), label='', required=False)

