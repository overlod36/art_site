from django.db import models
from users.models import Teacher_Profile, Study_Group

class Course(models.Model):
    title = models.CharField(verbose_name='Название дисциплины', max_length=50)
    author = models.ForeignKey(Teacher_Profile, null=False, verbose_name='Автор курса',on_delete=models.CASCADE)
    groups = models.ManyToManyField(Study_Group, blank=True, verbose_name='Группы')
    description = models.TextField(verbose_name='Описание курса')

    def __str__(self):
        return f"Курс: {self.title}, преподаватель: {self.author}"