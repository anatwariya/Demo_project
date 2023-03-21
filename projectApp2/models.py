from django.db import models

from projectApp3.models import CarPart


class Car(models.Model):
    model_name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    color = models.CharField(max_length=20, blank=False, null=False)
    parts_available = models.ManyToManyField(CarPart, related_name="related_cars_parts")
