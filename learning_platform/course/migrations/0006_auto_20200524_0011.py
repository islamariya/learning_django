# Generated by Django 3.0.3 on 2020-05-23 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20200421_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseflows',
            name='is_over',
        ),
        migrations.AddField(
            model_name='courseflows',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Поток завершен'),
        ),
    ]
