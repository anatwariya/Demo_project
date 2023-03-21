from django.db import models


class Car(models.Model):
    model_name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    color = models.CharField(max_length=20, blank=False, null=False)
