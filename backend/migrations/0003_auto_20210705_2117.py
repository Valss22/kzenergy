# Generated by Django 3.2.4 on 2021-07-05 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_gasturbineofcompressors_gasturbinepowerplant_highpressureboiler'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gasturbineofcompressors',
            old_name='gas_composition',
            new_name='gasComposition',
        ),
        migrations.RenameField(
            model_name='gasturbineofcompressors',
            old_name='gas_consumption_volume',
            new_name='gasConsumptionVolume',
        ),
        migrations.RenameField(
            model_name='gasturbineofcompressors',
            old_name='volume_of_injected_gas',
            new_name='volumeOfInjectedGas',
        ),
        migrations.RenameField(
            model_name='gasturbineofcompressors',
            old_name='waste_gases',
            new_name='wasteGases',
        ),
        migrations.RenameField(
            model_name='gasturbineofcompressors',
            old_name='working_hours',
            new_name='workingHours',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='full_name',
            new_name='fullName',
        ),
        migrations.AddField(
            model_name='gasturbineofcompressors',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='gasturbineofcompressors',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.user'),
        ),
    ]
