# Generated by Django 4.0.4 on 2022-04-15 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_fine_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='reason',
            field=models.CharField(default='parking', max_length=800),
        ),
    ]
