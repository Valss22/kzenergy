# Generated by Django 3.2.4 on 2021-07-05 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_gasturbineofcompressors_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasturbineofcompressors',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 5, 22, 9, 47, 445493), null=True),
        ),
    ]
