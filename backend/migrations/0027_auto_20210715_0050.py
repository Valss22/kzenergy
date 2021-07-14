# Generated by Django 3.2.4 on 2021-07-14 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_auto_20210714_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boiler',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.user'),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.user'),
        ),
        migrations.AlterField(
            model_name='powerplant',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.user'),
        ),
    ]
