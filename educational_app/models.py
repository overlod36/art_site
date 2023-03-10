from django.db import models
from users.models import Teacher_Profile, Study_Group

class Course(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Teacher_Profile, null=False, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Study_Group, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"Курс '{self.title}', преподаватель - {self.author}"