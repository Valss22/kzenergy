# Generated by Django 3.2.4 on 2021-09-01 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0044_auto_20210830_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
