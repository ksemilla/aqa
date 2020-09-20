import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from aqa.quotations.models import Quotation
from .models import Product

class ProductListCreateView(APIView):

    def get(self, request):
        list_of_products = []
        products = Product.objects.all()
        for product in products:
            list_of_products.append(
                {
                    "Product ID": product.id,
                    "Model Name": product.model_name,
                    "Description": product.description,
                    "SRP": product.sell_price,
                    "Capacity": product.capacity,
                }
            )
        return Response(list_of_products, status=200)


    def post(self, request):
        data = copy.deepcopy(request.data)

        # Check duplicates here
        pass

        # Check input completion. Must have unique model_name and description
        pass

        new_product = Product.objects.create(
            model_name=data["model_name"],
            description=data["description"],
            sell_price=data["sell_price"] if "sell_price" in data else 0,
            cost_price=data["cost_price"] if "cost_price" in data else 0, 
            stock_qty=data["stock_qty"] if "stock_qty" in data else 0,
            capacity=data["capacity"] if "capacity" in data else "",
        )

        content = {
            "success": f"New product {model_name} - {description} created"
        }

        return Response(content, status=200)