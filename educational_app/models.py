from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import Teacher_Profile, Study_Group, Student_Profile
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
import os
import shutil
from pathlib import Path
from . import file_methods
from educational_art_site.choices import *
import datetime
from django.core.exceptions import ValidationError

class Course(models.Model):
    title = models.CharField(verbose_name='Название дисциплины', max_length=50)
    code_name = models.CharField(blank=True, unique=True, max_length=50)
    author = models.ForeignKey(Teacher_Profile, null=False, verbose_name='Автор курса',on_delete=models.CASCADE)
    groups = models.ManyToManyField(Study_Group, blank=True, verbose_name='Группы')
    description = models.TextField(verbose_name='Описание курса')

    def save(self, *args, **kwargs):
        if not self.code_name:
            self.code_name = file_methods.get_transliteration(getattr(self, 'title'))
        file_methods.create_folder(os.path.join(file_methods.PATH, 'content', self.code_name, 'lectures'))
        file_methods.create_folder(os.path.join(file_methods.PATH, 'content', self.code_name, 'tests'))
        file_methods.create_folder(os.path.join(file_methods.PATH, 'content', self.code_name, 'tasks'))
        super(Course, self).save(*args, **kwargs)
    def __str__(self):
        return f"Курс: {self.title}, преподаватель: {self.author}"

class Lecture(models.Model):
    course = models.ForeignKey(Course, null=False, verbose_name='Дисциплина' ,on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_lecture_file_path, null=False, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])

    @property
    def filename(self):
        return str(os.path.basename(self.file.name))

class Test(models.Model):
    name = models.CharField(verbose_name='Название теста', max_length=50, blank=False)
    duration = models.DurationField(verbose_name='Длительность теста')
    course = models.ForeignKey(Course, null=False, verbose_name='Дисциплина', on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_test_file_path, null=False, validators=[FileExtensionValidator(['json'])])
    status = models.CharField(verbose_name="Статус теста", max_length=50, choices=TEST_STATUS)

    @property
    def filepath(self):
        return str(self.file.path)
    
class Test_Attempt(models.Model):
    test = models.ForeignKey(Test, null=False, verbose_name='Тест', on_delete=models.CASCADE)
    student = models.ForeignKey(Student_Profile, null=False, verbose_name='Студент', on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_test_attempt_file_path, null=False, validators=[FileExtensionValidator(['json'])])
    status = models.CharField(verbose_name="Статус решения теста", max_length=50, choices=TEST_ATTEMPT_STATUS)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата попытки')

    def save(self, *args, **kwargs):
        if self._state.adding: self.status = "CHECK"
        super(Test_Attempt, self).save(*args, **kwargs)

    @property
    def filepath(self):
        return str(self.file.path)

class Mark(models.Model):
    points = models.PositiveIntegerField()
    max_points = models.PositiveIntegerField()
    student = models.ForeignKey(Student_Profile, null=False, verbose_name='Студент', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Test_Mark(Mark):
    test = models.ForeignKey(Test, null=False, verbose_name='Тест', on_delete=models.CASCADE)
    test_attempt = models.OneToOneField(Test_Attempt, null=True, verbose_name='Попытка выполнения теста', on_delete=models.CASCADE)

@receiver(pre_delete, sender=Lecture)
def delete_lecture_file(sender, instance, *args, **kwargs):
    if instance.file: instance.file.delete()

@receiver(pre_delete, sender=Course)
def delete_course_folder(sender, instance, *args, **kwargs):
    course_path = os.path.join(file_methods.PATH, 'content', instance.code_name)
    file_methods.remove_folder(os.path.join(course_path, 'lectures'))
    file_methods.remove_folder(os.path.join(course_path, 'tests'))
    file_methods.remove_folder(os.path.join(course_path, 'tasks'))
    file_methods.remove_folder(course_path)

@receiver(pre_delete, sender=Test)
def delete_test_file(sender, instance, *args, **kwargs):
    if instance.file: instance.file.delete()
    file_methods.remove_tree(os.path.join(file_methods.PATH, 'content', file_methods.get_transliteration(getattr(instance.course, 'title')), 'tests', file_methods.get_transliteration(instance.name)))

@receiver(pre_delete, sender=Test_Attempt)
def delete_test_attempt_file(sender, instance, *args, **kwargs):
    if instance.file: instance.file.delete()

@receiver(pre_save, sender=Test)
def update_test(sender, instance, *args, **kwargs):
    if not instance._state.adding:
        if sender.objects.get(id=instance.id).name !=  instance.name:
            base_path = os.path.join(file_methods.PATH, 'content', file_methods.get_transliteration(getattr(instance.course, 'title')), 'tests')
            os.rename(os.path.join(base_path, file_methods.get_transliteration(sender.objects.get(id=instance.id).name), f'{file_methods.get_transliteration(sender.objects.get(id=instance.id).name)}.json'), 
                      os.path.join(base_path, file_methods.get_transliteration(sender.objects.get(id=instance.id).name), f'{file_methods.get_transliteration(instance.name)}.json'))
            os.rename(os.path.join(base_path, file_methods.get_transliteration(sender.objects.get(id=instance.id).name)), os.path.join(base_path, file_methods.get_transliteration(instance.name)))
            instance.file = os.path.join("%s" % instance.course.code_name, 'tests', file_methods.get_transliteration(instance.name), f'{file_methods.get_transliteration(instance.name)}.json')
        if sender.objects.get(id=instance.id).duration !=  instance.duration:
            print(instance.duration)

@receiver(post_save, sender=Lecture)
def lecture_announce(sender, instance, created, *args, **kwargs):
    if created: pass
