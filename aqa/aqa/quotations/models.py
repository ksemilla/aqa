from django.db import models
from django.utils import timezone
from aqa.users.models import User

from aqa.products.models import Product
from .const import QuotationDays

def quote_duration(duration=QuotationDays.QUOTE_DURATION):
    return timezone.now() + timezone.timedelta(days=duration)

class Quotation(models.Model):
    company_name = models.CharField(max_length=50, null=True, blank=True, default="")
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='quotations_as_author', on_delete=models.PROTECT)
    application_engr = models.ForeignKey(User, related_name='quotations_as_ae', on_delete=models.PROTECT, null=True)
    sales_engr = models.ForeignKey(User, related_name='quotations_as_se', on_delete=models.PROTECT, null=True)
    sales_lead = models.ForeignKey(User, related_name='quotations_as_sl', on_delete=models.PROTECT, null=True)
    expiry_date = models.DateTimeField(default=quote_duration)
    subject = models.CharField(max_length=50, null=True, blank=True, default="")
    sub_subject = models.CharField(max_length=50, default='Supply and Delivery of Air Conditioning Units')
    project = models.CharField(max_length=50, null=True, blank=True, default="")
    payment_terms = models.CharField(max_length=50, default='Full payment before delivery')
    location = models.CharField(max_length=50, default='Metro Manila')
    last_modified = models.ForeignKey(User, related_name='quotations_modified', on_delete=models.PROTECT, null=True)
    discount_rate = models.IntegerField(default=0)
    discount_amount = models.IntegerField(default=0)


    # explore .save method to polish the fields on subject, sub_subject, project

    @property
    def total_price(self):
        total_price = 0
        for item in self.quotationitem_set.all():
            total_price += item.quantity * item.product.sell_price
        return total_price

    @property
    def total_cost(self):
        total_cost = 0
        for item in self.quotationitem_set.all():
            total_cost += item.quantity * item.product.cost_price
        return total_cost


    def __str__(self):
        return f"Quote {self.id} - {self.company_name}"


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=200, null=True, blank=True, default="")
    line_number = models.PositiveIntegerField(default=1)
    lead_time = models.CharField(max_length=100, default="30-45 days")
    tagging = models.CharField(max_length=50, null=True, blank=True, default="")
    h_desc = models.PositiveIntegerField(default=1)


    @property
    def model_name(self):
        return self.product.model_name

    @property
    def sell_price(self):
        return self.product.sell_price

    @property
    def capacity(self):
        return self.product.capacity

    @property
    def cost_price(self):
        return self.product.cost_price

    def save(self, *args, **kwargs):
        if not self.pk and not self.tagging:  # initial creation
            self.tagging = f"FCU/ACCU-{self.line_number}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.tagging} {self.product} x {self.quantity} units from Quotation {self.quotation.id}"