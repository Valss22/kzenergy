# Generated by Django 3.2.4 on 2021-07-12 12:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_auto_20210712_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(default=datetime.datetime(2021, 7, 12, 18, 40, 34, 134029), max_length=50, null=True)),
                ('gasName', models.CharField(max_length=50, null=True)),
                ('density', models.FloatField(help_text='плотность газа', null=True)),
                ('nitrogen', models.FloatField(help_text='% масс N', null=True)),
                ('sulfur', models.FloatField(help_text='% масс S', null=True)),
                ('carbon', models.FloatField(help_text='% масс C', null=True)),
                ('LowerHeatCombustion', models.FloatField(help_text='ТГ, ГДж/т', null=True)),
                ('CO2EmissionFactor', models.FloatField(help_text='тСО2/ТДж', null=True)),
                ('CH4SpecificFactor', models.IntegerField(help_text='кг/ТДж', null=True)),
                ('N2OSpecificFactor', models.IntegerField(help_text='кг/ТДж', null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.RemoveField(
            model_name='gascomposition',
            name='user',
        ),
        migrations.RemoveField(
            model_name='powerplant',
            name='actualPower',
        ),
        migrations.AlterField(
            model_name='boiler',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 12, 18, 40, 34, 135030), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 12, 18, 40, 34, 134029), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='powerplant',
            name='date',
            field=models.CharField(default=datetime.datetime(2021, 7, 12, 18, 40, 34, 135030), max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='SummaryReport',
        ),
        migrations.AlterField(
            model_name='boiler',
            name='gasComposition',
            field=models.OneToOneField(help_text='г/с', null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.gas'),
        ),
        migrations.AlterField(
            model_name='compressor',
            name='gasComposition',
            field=models.OneToOneField(help_text='г/с', null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.gas'),
        ),
        migrations.AlterField(
            model_name='powerplant',
            name='gasComposition',
            field=models.OneToOneField(help_text='г/с', null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.gas'),
        ),
        migrations.DeleteModel(
            name='GasComposition',
        ),
    ]