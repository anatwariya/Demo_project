# Generated by Django 4.1.7 on 2023-03-22 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp1', '0003_user_active_user_car_part_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='NA', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default='user', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='user', max_length=50),
        ),
    ]
