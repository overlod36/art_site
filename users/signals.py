from django.db.models.signals import post_save
from .models import Student_Profile, Teacher_Profile, Admin_Profile
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_save, sender=Student_Profile)
def add_student_group(sender, instance, created, **kwargs):
    if created: instance.user.groups.add(Group.objects.get(name='Students'))

@receiver(post_save, sender=Teacher_Profile)
def add_teacher_group(sender, instance, created, **kwargs):
     if created: instance.user.groups.add(Group.objects.get(name='Teachers'))

@receiver(post_save, sender=Admin_Profile)
def add_admin_group(sender, instance, created, **kwargs):
     if created: instance.user.groups.add(Group.objects.get(name='Admins'))