from django.contrib import admin
from .models import Course, Lecture, Test
# Register your models here.

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Test)