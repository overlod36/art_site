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
from django_ckeditor_5.fields import CKEditor5Field

class Course(models.Model):
    title = models.CharField(verbose_name='Название дисциплины', max_length=50)
    code_name = models.CharField(blank=True, unique=True, max_length=50)
    author = models.ForeignKey(Teacher_Profile, null=False, verbose_name='Автор курса',on_delete=models.CASCADE)
    groups = models.ManyToManyField(Study_Group, blank=True, verbose_name='Группы')
    description = models.TextField(verbose_name='Описание курса')

    @property
    def groups_list(self):
        return self.groups.all()

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.code_name:
                self.code_name = file_methods.get_transliteration(getattr(self, 'title'))
            file_methods.create_folder(os.path.join(file_methods.PATH, 'content', 'educational_tapes', self.code_name, 'lectures'))
            file_methods.create_folder(os.path.join(file_methods.PATH, 'content', 'educational_tapes', self.code_name, 'tests'))
            file_methods.create_folder(os.path.join(file_methods.PATH, 'content', 'educational_tapes', self.code_name, 'tasks'))
        super(Course, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"Курс: {self.title}, преподаватель: {self.author}"

class Lecture(models.Model):
    course = models.ForeignKey(Course, null=False, verbose_name='Дисциплина' ,on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_lecture_file_path, null=False, validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'ppt', 'pptx'])])

    @property
    def filename(self):
        return str(os.path.basename(self.file.name))
    
    @property
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

class Task(models.Model):
    title = models.CharField(verbose_name='Название задания', max_length=50, blank=False)
    code_name = models.CharField(blank=True, unique=True, max_length=50)
    description = CKEditor5Field(config_name='extends')
    course = models.ForeignKey(Course, verbose_name='Дисциплина', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата задания')
    status = models.CharField(verbose_name="Статус задания", max_length=50, choices=TASK_STATUS)
    mark = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.status = 'PROCESS'
            if not self.code_name:
                self.code_name = file_methods.get_transliteration(getattr(self, 'title'))
            file_methods.create_folder(os.path.join(file_methods.PATH, 'content', 'educational_tapes', self.course.code_name, 'tasks', self.code_name))
        super(Task, self).save(*args, **kwargs)

class Task_Attempt(models.Model):
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.CASCADE)
    student = models.ForeignKey(Student_Profile, verbose_name='Студент', on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус решения задания", max_length=50, choices=TASK_ATTEMPT_STATUS)
    comment = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата выполнения задания')
    mark = models.PositiveIntegerField()

class Task_Attempt_File(models.Model):
    task_attempt = models.ForeignKey(Task_Attempt, verbose_name='Попытка задания', on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_methods.get_task_file_path)

    @property
    def filename(self):
        return str(os.path.basename(self.file.name))

class Test(models.Model):
    title = models.CharField(verbose_name='Название теста', max_length=150)
    duration = models.DurationField(verbose_name='Длительность теста')
    course = models.ForeignKey(Course, verbose_name='Дисциплина', on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус теста", max_length=50, choices=TEST_STATUS)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикация теста')

    @property
    def mark(self):
        total_points = 0
        for question in self.test_question_set.all():
            total_points += question.mark
        return total_points

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.status = 'PROCESS'
        super(Test, self).save(*args, **kwargs)

class Test_Question(models.Model):
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст вопроса', max_length=150)
    mark = models.PositiveIntegerField()

class Test_Answer(models.Model):
    question = models.ForeignKey(Test_Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Ответ')
    is_correct = models.BooleanField(default=False)

class Test_Attempt(models.Model):
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    student = models.ForeignKey(Student_Profile, verbose_name='Студент', on_delete=models.CASCADE)
    date_of_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата выполнения теста')
    status = models.CharField(verbose_name="Статус попытки", max_length=50, choices=TEST_ATTEMPT_STATUS)
    mark = models.PositiveIntegerField()

class Test_Attempt_Answer(models.Model):
    test_attempt = models.ForeignKey(Test_Attempt, verbose_name='Тестовая попытка', on_delete=models.CASCADE)
    question = models.ForeignKey(Test_Question, verbose_name='Тестовый вопрос', on_delete=models.CASCADE)
    answer = models.TextField(verbose_name='Ответ')
    is_correct = models.BooleanField()

    class Meta:
        unique_together = ('test_attempt', 'question')

@receiver(pre_delete, sender=Lecture)
def delete_lecture_file(sender, instance, *args, **kwargs):
    if instance.file: instance.file.delete()

@receiver(pre_delete, sender=Task_Attempt_File)
def delete_task_attempt_files(sender, instance, *args, **kwargs):
    if instance.file: instance.file.delete()

@receiver(pre_delete, sender=Task)
def delete_task_files(sender, instance, *args, **kwargs):
    task_path = os.path.join(file_methods.PATH, 'content', 'educational_tapes', instance.course.code_name, 'tasks', instance.code_name)
    file_methods.remove_folder(task_path)

@receiver(pre_delete, sender=Course)
def delete_course_folder(sender, instance, *args, **kwargs):
    course_path = os.path.join(file_methods.PATH, 'content', 'educational_tapes', instance.code_name)
    file_methods.remove_folder(os.path.join(course_path, 'lectures'))
    file_methods.remove_folder(os.path.join(course_path, 'tests'))
    file_methods.remove_folder(os.path.join(course_path, 'tasks'))
    file_methods.remove_folder(course_path)


@receiver(post_save, sender=Lecture)
def lecture_announce(sender, instance, created, *args, **kwargs):
    if created: pass

@receiver(post_save, sender=Test)
def status_test(sender, instance, created, *args, **kwargs):
    if created: instance.status = 'PROCESS'