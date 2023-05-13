from django.forms import Form, ModelForm
from django import forms
from .models import Test, Test_Question
from django.core.files import File
import json
import os
from . import file_methods
from django.core.validators import MaxValueValidator, MinValueValidator
from educational_art_site import choices

class TestShowForm(Form):

    def __init__(self, test, *args, **kwargs):
        super(TestShowForm, self).__init__(*args, **kwargs)
        self.questions = test.test_question_set.all()
        counter = 0
        for question in self.questions:
            if question.test_answer_set.all().count() > 1:
                choices = [(choice.text, choice.text) for choice in question.test_answer_set.all()]
                self.fields[f'{question.pk}'] = forms.ChoiceField(label=f'{question.text} ({question.mark} баллов)', required=True,
                                                                    choices=choices, widget=forms.RadioSelect)
            elif question.test_answer_set.all().count() == 1:
                self.fields[f'{question.pk}'] = forms.CharField(label=f'{question.text} ({question.mark} баллов)', widget=forms.Textarea)

class TestAttemptCheckForm(Form):
    def __init__(self, attempt, *args, **kwargs):
        super(TestAttemptCheckForm, self).__init__(*args, **kwargs)
        q_num = 0
        for answer in attempt.test_attempt_answer_set.all():
            q_num += 1
            points = 0
            if answer.is_correct: points = answer.question.mark
            self.fields[f'{answer.question.pk}'] = forms.IntegerField(label='', initial=points)
            self.fields[f'{answer.question.pk}'].widget.attrs['class'] = 'ans-input'
            self.fields[f'{answer.question.pk}'].widget.attrs['id'] = answer.question.pk
            self.fields[f'{answer.question.pk}'].widget.attrs['max'] = answer.question.mark
            self.fields[f'{answer.question.pk}'].widget.attrs['min'] = 0

class TestAttemptDeniedForm(Form):
    denied_st = forms.CharField(widget=forms.HiddenInput)

class TestPublishForm(Form):
    publish_st = forms.CharField(widget=forms.HiddenInput)

class TestInfoForm(ModelForm):
    info_st = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(TestInfoForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Название теста'
        self.fields['title'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['duration'].widget.attrs['class'] = 'form-control mb-2'

    class Meta:
        model = Test
        fields = ['title', 'duration']
        widgets = {'duration': forms.widgets.TimeInput(format='%H:%M:%S', attrs={'type': 'time'})}

class TestQuestionForm(Form):
    question_st = forms.CharField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Текст вопроса', 'class':'form-control mb-2 mt-4 question-input'}), label='')
    mark = forms.IntegerField(label='Количество баллов', widget=forms.NumberInput(attrs={'placeholder': 'Баллы', 'min': '1', 'class':'form-control mb-2 mark-input'}))
    answer = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Вариант ответа', 'class':'form-control mb-2 answer-input'}), label='')
    answer_correction = forms.ChoiceField(choices=choices.ANSWER_CORRECT, widget=forms.Select(attrs={'class':'form-control form-select mb-2'}))

    
