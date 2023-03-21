from django.db import models


class CarPart(models.Model):
    car_part_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    car_part_car_model = models.CharField(max_length=100, blank=False, null=False)
