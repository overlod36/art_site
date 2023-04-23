from django.db import models
from users.models import Student_Profile, Teacher_Profile
from django.db.models.signals import pre_delete, pre_save, post_save
from educational_art_site.choices import *

class Picture(models.Model):
    img = models.ImageField()
    title = models.CharField(verbose_name='Название картины', null = True, max_length=50)
    description = models.CharField(verbose_name='Описание картины', null = True, max_length=50)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации картины')

class Base_Gallery(models.Model):
    title = models.CharField(verbose_name='Название галереи', max_length=50, null=True)
    description = models.CharField(verbose_name='Описание галереи', max_length=50, null=True)

    class Meta:
        abstract = True

class Student_Gallery(Base_Gallery):
    student = models.OneToOneField(Student_Profile, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Видимость галереи", max_length=50, choices=STUDENT_GALLERY_VISIBILITY)

class Teacher_Gallery(Base_Gallery):
    teacher = models.OneToOneField(Teacher_Profile, on_delete=models.CASCADE)


