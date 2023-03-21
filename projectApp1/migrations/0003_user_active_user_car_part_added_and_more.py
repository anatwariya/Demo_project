# Generated by Django 4.1.7 on 2023-03-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp2', '0002_alter_car_color'),
        ('projectApp3', '0001_initial'),
        ('projectApp1', '0002_alter_user_email_alter_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='car_part_added',
            field=models.ManyToManyField(related_name='wanted_cars_parts', to='projectApp3.carpart'),
        ),
        migrations.AddField(
            model_name='user',
            name='car_part_purchased',
            field=models.ManyToManyField(related_name='purchased_cars_parts', to='projectApp3.carpart'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_cars',
            field=models.ManyToManyField(related_name='user_cars', to='projectApp2.car'),
        ),
    ]