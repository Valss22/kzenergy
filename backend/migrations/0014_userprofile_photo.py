# Generated by Django 3.1.6 on 2021-06-21 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_remove_userprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.JSONField(default={'large': None, 'small': None}, null=True),
        ),
    ]
