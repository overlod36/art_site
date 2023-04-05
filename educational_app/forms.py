from django.forms import Form
from django.forms import ChoiceField, RadioSelect, CharField, Textarea

class QuizShowForm(Form):
    
    def __init__(self, questions, *args, **kwargs):
        super(QuizShowForm, self).__init__(*args, **kwargs)
        self.questions = questions
        counter = 0
        for question in self.questions:
            counter += 1
            match question['type']:
                case 'TF':
                    self.fields[f'TF_field_{counter}'] = ChoiceField(label=question['text'], required=True, 
                                        choices=((True, 'Да'), (False, 'Нет')), widget=RadioSelect)
                case 'O':
                    self.fields[f'O_field_{counter}'] = CharField(label=question['text'], widget=Textarea) 
                case 'AO':
                    choices = [(i, question['choices'][i-1]) for i in range(1, len(question['choices']))]
                    self.fields[f'AO_field_{counter}'] = ChoiceField(label=question['text'], required=True,
                                           choices=choices, widget=RadioSelect)
        
