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
                    "id": product.id,
                    "model_name": product.model_name,
                    "description": product.description,
                    "sell_price": product.sell_price,
                    "capacity": product.capacity,
                }
            )
        return Response(list_of_products, status=200)


    def post(self, request):
        data = copy.deepcopy(request.data)

        # Check duplicates here. Must have unique model_name and description
        existing_products = Product.objects.values_list("model_name", "description")
        if (data["model_name"], data["description"]) in existing_products:
            return Response({"error": f"Product {data["model_name"]} - {data["description"]} is already existing"}, status=400)
        

        # Check input completion.
        required_fields = {"model_name", "description", "capacity"}
        # if any(field not in data for field in required_fields):
        missing_info = []
        for field in required_fields:
            if field not in data:
                missing_info.append(field)
        if missing_info:
            return Response({"error": f"Incomplete data. Please input: {missing_info}"}, status=400)

        new_product = Product.objects.create(
            model_name=data["model_name"],
            description=data["description"],
            sell_price=data["sell_price"] if "sell_price" in data else 0,
            cost_price=data["cost_price"] if "cost_price" in data else 0, 
            stock_qty=data["stock_qty"] if "stock_qty" in data else 0,
            capacity=data["capacity"],
        )

        content = {
            "success": f"Created new product: {new_product.model_name} - {new_product.description}"
        }

        return Response(content, status=200)