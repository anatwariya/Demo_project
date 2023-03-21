from django.db import models
from projectApp2.models import Car
from projectApp3.models import CarPart



class User(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    active = models.BooleanField(default=False)
    user_cars = models.ManyToManyField(Car, related_name="user_cars")
    car_part_purchased = models.ManyToManyField(CarPart, related_name="purchased_cars_parts")
    car_part_added = models.ManyToManyField(CarPart, related_name="wanted_cars_parts")
