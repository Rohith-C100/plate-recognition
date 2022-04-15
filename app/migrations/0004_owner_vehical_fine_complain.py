# Generated by Django 4.0.4 on 2022-04-15 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_number_plate_purpose'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_number', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('education', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vehical',
            fields=[
                ('plate_number', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Scooty', 'Scooty'), ('Luna', 'Luna'), ('Bike', 'Bike'), ('Auto Riksha', 'Auto Riksha'), ('Car', 'Car'), ('Bus', 'Bus'), ('Truck', 'Truck'), ('Tempo', 'Tempo'), ('Traveller', 'Traveller'), ('Lorry', 'Lorry'), ('Tractor', 'Tractor'), ('Heavy Vehicle', 'Heavy Vehicle')], max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('date_of_registration', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='fineimg/')),
                ('date', models.DateField()),
                ('details', models.CharField(max_length=800)),
                ('vehical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vehical')),
            ],
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('severity', models.CharField(choices=[('Extreme', 'Extreme'), ('moderate', 'moderate'), ('normal', 'normal')], max_length=100)),
                ('date_of_incident', models.DateField()),
                ('details', models.CharField(max_length=500)),
                ('vehical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vehical')),
            ],
        ),
    ]