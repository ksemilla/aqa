from django.db import models
from django.utils import timezone
from aqa.users.models import User

from aqa.products.models import Product

def quote_duration(duration=30):
    return timezone.now() + timezone.timedelta(days=duration)

class Quotation(models.Model):
    company_name = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='quotations_as_author', on_delete=models.PROTECT)
    application_engr = models.ForeignKey(User, related_name='quotations_as_ae', on_delete=models.PROTECT, null=True)
    sales_engr = models.ForeignKey(User, related_name='quotations_as_se', on_delete=models.PROTECT, null=True)
    sales_lead = models.ForeignKey(User, related_name='quotations_as_sl', on_delete=models.PROTECT, null=True)
    expiry_date = models.DateTimeField(default=quote_duration)
    subject = models.CharField(max_length=50, null=True)
    sub_subject = models.CharField(max_length=50, default='Supply and Delivery of Air Conditioning Units')
    project = models.CharField(max_length=50, null=True)
    payment_terms = models.CharField(max_length=50, default='Full payment before delivery')
    location = models.CharField(max_length=50, default='Metro Manila')
    last_modified = models.ForeignKey(User, related_name='quotations_modified', on_delete=models.PROTECT, null=True)

    # explore .save method to polish the fields on subject, sub_subject, project


    def __str__(self):
        return f"Quote {self.id} - {self.company_name}"

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Quotation Item {self.product} x {self.quantity} units from Quotation {self.quotation.id}"