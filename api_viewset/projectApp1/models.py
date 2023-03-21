from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)
