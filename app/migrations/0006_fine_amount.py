# Generated by Django 4.0.4 on 2022-04-15 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_owner_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='amount',
            field=models.IntegerField(choices=[('100', 100), ('500', 500), ('1000', 1000), ('2000', 2000), ('5000', 5000)], default=100),
        ),
    ]
