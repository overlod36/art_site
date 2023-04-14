from django.forms import Form, ModelForm
from django import forms
from .models import Test_Attempt, Test
from django.core.files import File
import json
import os
from . import file_methods

class QuizShowForm(Form):

    def __init__(self, questions, *args, **kwargs):
        super(QuizShowForm, self).__init__(*args, **kwargs)
        self.questions = questions
        counter = 0
        self.fields[f'quiz_show'] = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
        for question in self.questions:
            counter += 1
            match question['type']:
                case 'TF':
                    self.fields[f'TF_field_{counter}'] = forms.ChoiceField(label=f'{question["text"]} ({question["mark"]} баллов)', required=True, 
                                        choices=(('True', 'Да'), ('False', 'Нет')), widget=forms.RadioSelect)
                case 'O':
                    self.fields[f'O_field_{counter}'] = forms.CharField(label=f'{question["text"]} ({question["mark"]} баллов)', widget=forms.Textarea) 
                case 'AO':
                    choices = [(i, question['choices'][i-1]) for i in range(1, len(question['choices']) + 1)]
                    self.fields[f'AO_field_{counter}'] = forms.ChoiceField(label=f'{question["text"]} ({question["mark"]} баллов)', required=True,
                                           choices=choices, widget=forms.RadioSelect)
    
    def save(self, solution, user, test, *args, **kwargs):
        interm_file_path = os.path.join(file_methods.PATH, 'intermediate_content', 
                              f'{file_methods.get_transliteration(test.name)}.json')
        f = open(interm_file_path, 'a+', encoding='utf-8')
        res_str = json.dumps(solution, indent = 2, ensure_ascii=False)
        f.write(res_str)
        test_attempt = Test_Attempt(test=test, student=user.student_profile, file=File(f))
        test_attempt.save()
        f.close()
        os.remove(interm_file_path)

class QuizUpdateForm(ModelForm):
    
    class Meta:
        model = Test
        fields = ['name', 'duration']
        widgets = {'duration': forms.widgets.TimeInput(attrs={'type': 'time'})}

class QuizPublishForm(Form):
    publish_st = forms.CharField(widget=forms.HiddenInput)

