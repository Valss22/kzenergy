# Generated by Django 3.2.4 on 2021-07-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20210703_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='password is hashed', max_length=128, null=True, verbose_name='password'),
        ),
    ]
