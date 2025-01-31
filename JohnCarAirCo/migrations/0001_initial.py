# Generated by Django 4.1.7 on 2023-03-27 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirconType',
            fields=[
                ('airconType', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerName', models.CharField(max_length=255)),
                ('customerContact', models.CharField(max_length=12)),
                ('customerEmail', models.CharField(max_length=255)),
                ('customerAddress', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unitName', models.CharField(max_length=255)),
                ('unitPrice', models.DecimalField(decimal_places=2, max_digits=12)),
                ('unitStocks', models.IntegerField()),
                ('unitType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='JohnCarAirCo.aircontype')),
            ],
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOrdered', models.DateField(auto_now_add=True)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Finished', 'Finished'), ('Cancelled', 'Cancelled')], default='Active', max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JohnCarAirCo.customerdetails')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOrdered', models.DateField(auto_now_add=True)),
                ('serviceDate', models.DateField()),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Finished', 'Finished'), ('Cancelled', 'Cancelled')], default='Active', max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JohnCarAirCo.customerdetails')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceName', models.CharField(max_length=50)),
                ('serviceCost', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='TechnicianDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('techName', models.CharField(max_length=255)),
                ('techPhone', models.CharField(max_length=12)),
                ('techEmail', models.CharField(max_length=255)),
                ('techSched', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOrderEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='JohnCarAirCo.serviceorder')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JohnCarAirCo.servicetype')),
            ],
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JohnCarAirCo.techniciandetails'),
        ),
        migrations.CreateModel(
            name='SalesOrderEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='JohnCarAirCo.salesorder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JohnCarAirCo.productunit')),
            ],
        ),
    ]
