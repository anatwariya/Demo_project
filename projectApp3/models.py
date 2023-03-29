from django.db import models


class CarPart(models.Model):
    img_url = models.CharField(max_length=500, default="https://thumbs.dreamstime.com/z/vector-car-parts-turbocharger-isolated-white-background-vector-car-parts-turbocharger-145918739.jpg")
    car_part_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    price = models.IntegerField(default=0)
