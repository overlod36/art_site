from django.db import models
from educational_app.models import Course
from datetime import datetime

class Course_Announce(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # удалять ли, когда удалится преподаватель?
    publish_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'Объявление -> {self.title}, дисциплина -> {self.course}'