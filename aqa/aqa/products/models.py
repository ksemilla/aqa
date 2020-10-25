from django.db import models

class Product(models.Model):
    model_name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    sell_price = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0)
    stock_qty = models.IntegerField(default=0)
    capacity = models.CharField(null=True, max_length=20)
    electrical = models.CharField(max_length=20, default="230V-1Ph-60Hz")

    def __str__(self):
        return self.model_name