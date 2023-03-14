from django.db import models
from educational_app.models import Course
from datetime import datetime

class Course_Announce(models.Model):
    title = models.CharField(verbose_name= 'Заголовок объявления', max_length=50)
    text = models.TextField(verbose_name='Текст объявления')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Дисциплина') # удалять ли, когда удалится преподаватель?
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'Объявление -> {self.title}, дисциплина -> {self.course}'