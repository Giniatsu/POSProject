# Generated by Django 4.1.7 on 2023-02-25 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JohnCarAirCo', '0008_rename_customer_salesorder_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesorder',
            old_name='customer_id',
            new_name='customer',
        ),
    ]
