# Generated by Django 4.1.7 on 2023-03-13 01:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('JohnCarAirCo', '0012_serviceorder_technician'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='serviceDate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
