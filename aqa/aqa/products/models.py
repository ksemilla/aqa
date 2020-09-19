from django.db import models

class Product(models.Model):
    model_name = models.CharField(max_length=200, null=True, blank=True)