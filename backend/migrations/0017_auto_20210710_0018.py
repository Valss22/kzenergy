# Generated by Django 3.2.4 on 2021-07-09 18:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20210709_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boiler',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 10, 0, 18, 40, 849400), null=True),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 10, 0, 18, 40, 848399), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='gascomposition',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 10, 0, 18, 40, 848399), null=True),
        ),
        migrations.AlterField(
            model_name='powerplant',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 10, 0, 18, 40, 849400), null=True),
        ),
    ]
