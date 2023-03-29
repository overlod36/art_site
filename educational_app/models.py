from django.db import models
from users.models import Teacher_Profile, Study_Group
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os
from pathlib import Path

PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

def transliterate(string):
    char_dict = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', ',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
    
    for key in char_dict:
        string = string.replace(key, char_dict[key])
    return string

def get_file_path(instance, filename):
    return os.path.join("%s" % instance.course.code_name, filename)

def get_transliteration(title):
    return transliterate(title.lower())

class Course(models.Model):
    title = models.CharField(verbose_name='Название дисциплины', max_length=50)
    code_name = models.CharField(blank=True, unique=True, max_length=50)
    author = models.ForeignKey(Teacher_Profile, null=False, verbose_name='Автор курса',on_delete=models.CASCADE)
    groups = models.ManyToManyField(Study_Group, blank=True, verbose_name='Группы')
    description = models.TextField(verbose_name='Описание курса')

    def save(self, *args, **kwargs):
        if not self.code_name:
            self.code_name = get_transliteration(getattr(self, 'title'))
        os.makedirs(os.path.join(PATH, 'content', self.code_name))
        super(Course, self).save(*args, **kwargs)
    def __str__(self):
        return f"Курс: {self.title}, преподаватель: {self.author}"

class Lecture(models.Model):
    course = models.ForeignKey(Course, null=False, verbose_name='Дисциплина' ,on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_path)


@receiver(pre_delete, sender=Lecture)
def delete_lecture_file(sender, instance, *args, **kwargs):
    if instance.file: instance.file.delete()

@receiver(pre_delete, sender=Course)
def delete_course_folder(sender, instance, *args, **kwargs):
    Path(os.path.join(PATH, 'content', instance.code_name)).rmdir()
    # if os.path.isfile(path): os.remove(path)