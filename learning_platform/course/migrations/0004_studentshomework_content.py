# Generated by Django 3.0.3 on 2020-04-16 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_course_main_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentshomework',
            name='content',
            field=models.TextField(default='', max_length=300, verbose_name='Содержание'),
        ),
    ]
