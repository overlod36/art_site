from django.db import models
from educational_app.models import Course
from datetime import datetime
from users.models import Teacher_Profile, Admin_Profile
from django_ckeditor_5.fields import CKEditor5Field

class Base_Announce(models.Model):
    title = models.CharField(verbose_name= 'Заголовок объявления', max_length=50)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        abstract = True

class Course_Announce(Base_Announce):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Дисциплина') # удалять ли, когда удалится преподаватель?
    text = models.TextField(verbose_name='Текст объявления')

    def __str__(self):
        return f'Учебное объявление -> {self.title}, дисциплина -> {self.course}'

class News_Announce(Base_Announce):
    author = models.ForeignKey(Teacher_Profile, null=False, verbose_name='Автор новости', on_delete=models.CASCADE)
    html = CKEditor5Field(config_name='extends')

    def __str__(self):
        return f'Новостное объявление -> { self.title }, автор новости -> { self.author }'

class System_Announce(Base_Announce):
    author = models.ForeignKey(Admin_Profile, null=False, verbose_name='Автор объявления', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст объявления')

    def __str__(self):
        return f'Системное объявление -> { self.title }, автор объявления -> { self.author }'