# Generated by Django 4.1 on 2023-03-27 22:32

from django.db import migrations, models
import django.db.models.deletion
import educational_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('educational_app', '0004_alter_course_author_alter_course_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=educational_app.models.get_file_path)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educational_app.course', verbose_name='Дисциплина')),
            ],
        ),
    ]
