# Generated by Django 3.2.4 on 2021-07-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_auto_20210714_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boiler',
            name='date',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='date',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='powerplant',
            name='date',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]