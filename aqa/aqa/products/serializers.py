from rest_framework import serializers

from aqa.products.models import (
    Product,
)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id', 'model_name', 'description', 'sell_price', 'cost_price', 'capacity', 'stock_qty',
        )