from django.contrib import admin
from .models import Student_Gallery, Student_Picture, Teacher_Picture, Teacher_Gallery

admin.site.register(Student_Gallery)
admin.site.register(Teacher_Gallery)
admin.site.register(Student_Picture)
admin.site.register(Teacher_Picture)


