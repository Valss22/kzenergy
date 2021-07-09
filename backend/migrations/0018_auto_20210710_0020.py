# Generated by Django 3.2.4 on 2021-07-09 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20210710_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boiler',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 10, 0, 20, 37, 530258), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 10, 0, 20, 37, 529248), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='gascomposition',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 10, 0, 20, 37, 528246), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='powerplant',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 10, 0, 20, 37, 529248), max_length=50, null=True),
        ),
    ]