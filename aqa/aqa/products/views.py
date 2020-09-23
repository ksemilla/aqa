import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

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

        # Check input completion.
        required_fields = {"model_name", "description", "capacity"}
        # if any(field not in data for field in required_fields):
        missing_info = []
        for field in required_fields:
            if field not in data:
                missing_info.append(field)
        if missing_info:
            return Response({"error": f"Incomplete data. Please input: {missing_info}"}, status=400)

        
        if Product.objects.filter(model_name=data["model_name"]) and Product.objects.filter(description=data["description"]):
            return Response({"error": f"Product {data['model_name']} - {data['description']} already existing"}, status=400)
        

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



class ProductFetchUpdateDestroy(APIView):
    
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=400)

        context = {
            "id": product.id,
            "model_name": product.model_name,
            "capacity": product.capacity,
            "sell_price": product.sell_price,
            "description": product.description,
        }
        return Response(context, status=200)


    def put(self, request, pk):
            data = copy.deepcopy(request.data)
            product = Product.objects.filter(pk=pk).first()
            
            if not product:
                return Response({"error": f"Product code {pk} does not exists"}, status=400)

            product.model_name = data["model_name"] if 'model_name' in data else product.model_name
            product.description = data['description'] if 'description' in data else product.description
            product.capacity = data['capacity'] if 'capacity' in data else product.capacity
            product.sell_price = data['sell_price'] if 'sell_price' in data else product.sell_price
            product.cost_price = data['cost_price'] if 'cost_price' in data else product.cost_price
            product.save()
            return Response({"success": f"Saved changes in product {product.id}"}, status=200)

    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=400)
        temp_id = product.id
        product.delete()

        return Response({"success": f"deleted Product code {temp_id}"})