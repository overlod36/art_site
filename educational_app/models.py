from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import Teacher_Profile, Study_Group, Student_Profile
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os
import shutil
from pathlib import Path
from . import file_methods

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
    # duration = models.DurationField(verbose_name='Длительность теста')
    # expiration_date = models.DateTimeField(verbose_name='Срок сдачи')
    course = models.ForeignKey(Course, null=False, verbose_name='Дисциплина', on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_test_file_path, null=False, validators=[FileExtensionValidator(['json'])])

    @property
    def filepath(self):
        return str(self.file.path)

class Test_Attempt(models.Model):
    test = models.ForeignKey(Test, null=False, verbose_name='Тест', on_delete=models.CASCADE)
    student = models.ForeignKey(Student_Profile, null=False, verbose_name='Студент', on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_test_attempt_file_path, null=False, validators=[FileExtensionValidator(['json'])])

    @property
    def filepath(self):
        return str(self.file.path)

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
