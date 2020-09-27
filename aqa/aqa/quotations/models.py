from django.db import models
from django.utils import timezone
from aqa.users.models import User

from aqa.products.models import Product

def quote_duration(duration=30):
    return timezone.now() + timezone.timedelta(days=duration)

class Quotation(models.Model):
    company_name = models.CharField(blank=False, null=True, max_length=50)
    created_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # expiry_date = models.DateField(blank=True, null=True, default=quote_duration)

    def __str__(self):
        return f"Quote {self.id} - {self.company_name}"

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, blank=True, null=True)
    line_number = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Quotation Item {self.product} x {self.quantity} units"