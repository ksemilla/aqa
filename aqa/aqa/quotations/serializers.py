from rest_framework import serializers

from aqa.quotations.models import (
    Quotation,
    QuotationItem
)

from aqa.users.serializers import UserSerializer

class QuotationSerializer(serializers.ModelSerializer):
    author_detail = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_author_detail(self, obj):
        user_author = obj.author
        return UserSerializer(user_author).data

    def get_items(self, obj):
        quotation_items = obj.quotationitem_set.all() # query set
        return QuotationItemSerializer(quotation_items, many=True).data

    class Meta:
        model = Quotation
        fields = (
            'id', 'company_name', 'created_date', 'author', 'author_detail', 'items',
        )

class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = (
            'id', 'quotation', 'product', 'quantity'
        )