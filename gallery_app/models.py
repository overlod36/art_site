from django.db import models
from users.models import Student_Profile, Teacher_Profile
from django.db.models.signals import pre_delete, pre_save, post_save
from educational_art_site.choices import *
from django.dispatch.dispatcher import receiver
from . import file_methods
import os
from PIL import Image

class Base_Gallery(models.Model):
    title = models.CharField(verbose_name='Название галереи', max_length=150, null=True)
    description = models.CharField(verbose_name='Описание галереи', max_length=650, null=True)

    class Meta:
        abstract = True

class Student_Gallery(Base_Gallery):
    student = models.OneToOneField(Student_Profile, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Видимость галереи", max_length=50, choices=STUDENT_GALLERY_VISIBILITY)

    @property
    def pictures_count(self):
        return self.student_picture_set.all().count()

    @property
    def cover(self):
        return self.student_picture_set.latest('publish_date')

    def __str__(self):
        return f'Галерея студента {self.student.last_name} {self.student.first_name}'

class Teacher_Gallery(Base_Gallery):
    teacher = models.OneToOneField(Teacher_Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Галерея преподавателя {self.teacher.first_name} {self.teacher.last_name}'

class Public_Gallery(Base_Gallery):
    author = models.ForeignKey(Teacher_Profile, on_delete=models.CASCADE)
    code_name = models.CharField(blank=True, unique=True, max_length=150)

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.code_name:
                self.code_name = file_methods.get_transliteration(getattr(self, 'title'))
            file_methods.create_folder(os.path.join(file_methods.PATH, 'content', 'public_galleries', self.code_name))
        super(Public_Gallery, self).save(*args, **kwargs)

    @property
    def pictures_count(self):
        return self.public_picture_set.all().count()
    
    @property
    def cover(self):
        return self.public_picture_set.latest('publish_date')

    def __str__(self):
        return f'Публичная галерея за авторством {self.author.last_name} {self.author.first_name}'


class Base_Picture(models.Model):
    title = models.CharField(verbose_name='Название картины', null = True, max_length=150)
    description = models.CharField(verbose_name='Описание картины', null = True, max_length=650)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации картины')

    class Meta:
        abstract = True

class Public_Picture(Base_Picture):
    public_img = models.ImageField(upload_to=file_methods.get_public_pic_path)
    public_gallery = models.ForeignKey(Public_Gallery, on_delete=models.CASCADE)
        
    @property
    def pic_size(self):
        return self.public_img.file.size

    def __str__(self):
        return f'Изображение {self.public_gallery}'

class Student_Picture(Base_Picture):
    student_img = models.ImageField(upload_to=file_methods.get_student_pic_path)
    student_gallery = models.ForeignKey(Student_Gallery, on_delete=models.CASCADE)
        
    @property
    def pic_size(self):
        return self.student_img.file.size

    def __str__(self):
        return f'Изображение студента {self.student_gallery.student.first_name} {self.student_gallery.student.last_name}'

class Teacher_Picture(Base_Picture):
    teacher_img = models.ImageField()
    teacher_gallery = models.ForeignKey(Teacher_Gallery, on_delete=models.CASCADE)

    def __str__(self):
        return f'Изображение преподавателя {self.teacher_gallery.teacher.first_name} {self.teacher_gallery.teacher.last_name}'

# @receiver(post_save, sender=Student_Picture)
# def st_pic_compress(sender, instance, *args, **kwargs):
#     if instance.student_img.file.size > file_methods.PIC_SIZE_RESTR:
#             new_img = Image.open(instance.student_img.path)
#             new_img.save(instance.student_img.path, quality=100, subsampling=0)
#             new_img.close()

@receiver(post_save, sender=Student_Gallery)
def st_gallery_create(sender, instance, created, *args, **kwargs):
    if created: file_methods.create_folder(os.path.join(file_methods.PATH, 'content', 'student_galleries', f'{instance.student.user.username}'))

@receiver(pre_delete, sender=Student_Picture)
def st_pic_delete(sender, instance, *args, **kwargs):
    if instance.student_img: instance.student_img.delete()

@receiver(pre_delete, sender=Student_Gallery)
def st_gallery_delete(sender, instance, *args, **kwargs):
    file_methods.remove_folder(os.path.join(file_methods.PATH, 'content', 'student_galleries', f'{instance.student.user.username}'))

@receiver(pre_delete, sender=Public_Picture)
def pub_pic_delete(sender, instance, *args, **kwargs):
    if instance.public_img: instance.public_img.delete()

@receiver(pre_delete, sender=Public_Gallery)
def public_gallery_delete(sender, instance, *args, **kwargs):
    file_methods.remove_folder(os.path.join(file_methods.PATH, 'content', 'public_galleries', f'{instance.code_name}'))