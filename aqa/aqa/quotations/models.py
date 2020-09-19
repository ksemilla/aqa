from django.db import models
from django.utils import timezone
from aqa.users.models import User


class Quotation(models.Model):
    company_name = models.CharField(blank=True, null=True, max_length=50)
    created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.CharField(blank=True, null=True, max_length=15)