from django.db import models
from educational_app.models import Course
from datetime import datetime
from users.models import Teacher_Profile, Admin_Profile

class Course_Announce(models.Model):
    title = models.CharField(verbose_name= 'Заголовок объявления', max_length=50)
    text = models.TextField(verbose_name='Текст объявления')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Дисциплина') # удалять ли, когда удалится преподаватель?
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'Учебное объявление -> {self.title}, дисциплина -> {self.course}'

class News_Announce(models.Model):
    title = models.CharField(verbose_name= 'Заголовок новости', max_length=50)
    text = models.TextField(verbose_name='Текст новости')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(Teacher_Profile, null=False, verbose_name='Автор новости', on_delete=models.CASCADE)

    def __str__(self):
        return f'Новостное объявление -> { self.title }, автор новости -> { self.author }'

class System_Announce(models.Model):
    title = models.CharField(verbose_name= 'Заголовок объявления', max_length=50)
    text = models.TextField(verbose_name='Текст объявления')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(Admin_Profile, null=False, verbose_name='Автор объявления', on_delete=models.CASCADE)

    def __str__(self):
        return f'Системное объявление -> { self.title }, автор объявления -> { self.author }'