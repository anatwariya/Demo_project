# Generated by Django 4.1.7 on 2023-03-22 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp3', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carpart',
            name='car_part_car_model',
        ),
        migrations.AddField(
            model_name='carpart',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
