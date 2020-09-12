from django.db import models
from django.utils import timezone
# Create your models here.

class Quotation(models.Model):
    created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    author = models.CharField(blank=True, null=True, max_length=256)
    expiry_date = models.CharField(blank=True, null=True, max_length=15)
    