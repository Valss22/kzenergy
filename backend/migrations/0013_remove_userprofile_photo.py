# Generated by Django 3.1.6 on 2021-06-21 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_userprofile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='photo',
        ),
    ]
