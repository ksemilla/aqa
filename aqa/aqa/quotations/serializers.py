from rest_framework import serializers

from aqa.quotations.models import (
    Quotation,
    QuotationItem
)

from aqa.users.serializers import UserSerializer

class QuotationSerializer(serializers.ModelSerializer):
    author_detail = serializers.SerializerMethodField()
    ae_detail = serializers.SerializerMethodField()
    se_detail = serializers.SerializerMethodField()
    sl_detail = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_author_detail(self, obj):
        user_author = obj.author
        return UserSerializer(user_author).data

    def get_ae_detail(self, obj):
        ae = obj.application_engr
        return UserSerializer(ae).data

    def get_se_detail(self, obj):
        se = obj.sales_engr
        return UserSerializer(se).data

    def get_sl_detail(self, obj):
        sl = obj.sales_lead
        return UserSerializer(sl).data

    def get_items(self, obj):
        quotation_items = obj.quotationitem_set.all() # query set
        return QuotationItemSerializer(quotation_items, many=True).data

    class Meta:
        model = Quotation
        fields = (
            'id', 'company_name', 'created_date', 'author', 'application_engr', 'sales_engr', 
            'sales_lead', 'author_detail', 'ae_detail', 'se_detail', 'sl_detail', 'items', 'expiry_date', 
            'subject', 'sub_subject', 'project', 'payment_terms', 'location', 'last_modified', 'discount', 
            'total_price', 'total_cost',
        )

class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = (
            'id', 'quotation', 'product', 'quantity', 'line_number', 'description', 'lead_time', 'tagging', 
            'model_name', 'sell_price', 'capacity', 'cost_price',
        )

class CreateQuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = (
            'id', 'product', 'quantity', 'line_number', 'description', 'lead_time', 'tagging', 'model_name',
            'sell_price', 'capacity', 'cost_price',
        )