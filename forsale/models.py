from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=256, blank=True)

