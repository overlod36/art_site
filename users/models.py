from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
import gallery_app.models

class Study_Group(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер группы', unique=True)

    def __str__(self):
        return f'Группа {self.number}'

class Base_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name= 'Имя', max_length=20, blank=True)
    last_name = models.CharField(verbose_name= 'Фамилия', max_length=30, blank=True)
    sur_name = models.CharField(verbose_name="Отчество",max_length=30, blank=True)

    class Meta:
        abstract = True

class Teacher_Profile(Base_Profile):
    def __str__(self):
        return f'Преподаватель {self.last_name} {self.first_name}'

class Student_Profile(Base_Profile):
    group = models.ForeignKey(Study_Group, verbose_name= 'Группа', null=True, on_delete=models.SET_NULL) # вопрос, как быть с удалением групп и переопределением

    def __str__(self):
        return f'Студент {self.last_name} {self.first_name}'

class Admin_Profile(Base_Profile):
    def __str__(self):
        return f'Администратор {self.user.username}'
    
@receiver(post_save, sender=Student_Profile)
def create_gallery(sender, instance, created, *args, **kwargs):
    if created:
        gal = gallery_app.models.Student_Gallery(student=instance, status='PRIVATE')
        gal.save()
