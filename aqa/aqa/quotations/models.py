from django.db import models
from django.utils import timezone
from aqa.users.models import User

def quote_duration(duration=30):
    return timezone.now() + timezone.timedelta(days=duration)

class Quotation(models.Model):
    company_name = models.CharField(blank=False, null=False, max_length=50)
    created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(blank=True, null=True, default=quote_duration)

    def __str__(self):
        return f"Quote {self.id} for {self.company_name}"