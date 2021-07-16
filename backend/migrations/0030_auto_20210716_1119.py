# Generated by Django 3.2.4 on 2021-07-16 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_auto_20210715_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='boiler',
            name='isRefused',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='compressor',
            name='isRefused',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='powerplant',
            name='isRefused',
            field=models.BooleanField(default=False),
        ),
    ]
