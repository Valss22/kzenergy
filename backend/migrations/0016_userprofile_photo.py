# Generated by Django 3.1.6 on 2021-06-21 09:28

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_remove_userprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.JSONField(default=backend.models.json_default, null=True),
        ),
    ]
