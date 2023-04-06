from django.contrib import admin
from .models import Course, Lecture, Test, Test_Attempt
# Register your models here.

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Test)
admin.site.register(Test_Attempt)