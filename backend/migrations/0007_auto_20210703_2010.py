# Generated by Django 3.2.4 on 2021-07-03 14:10

import backend.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20210703_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('full_name', models.CharField(max_length=100, null=True, validators=[backend.validators.validate_full_name])),
                ('role', models.CharField(max_length=100, null=True, validators=[backend.validators.validate_role])),
                ('password', models.CharField(max_length=128, null=True, verbose_name='password')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='backend.user'),
        ),
    ]
