import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(ListCreateAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def create(self, request):
        data = copy.deepcopy(request.data)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            product.save()

            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
    def retrieve(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        
    
    def update(self, request, pk):
        data = copy.deepcopy(request.data)
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            for attr, value in data.items():
                setattr(product, attr, value)
                product.save()
        return Response({"success": f"Saved changes in product {product.model_name}", "new_data": ProductSerializer(product).data}, status=status.HTTP_200_OK)
        



    # def put(self, request, pk):
    #         data = copy.deepcopy(request.data)
    #         product = Product.objects.filter(pk=pk).first()
            
    #         if not product:
    #             return Response({"error": f"Product code {pk} does not exists"}, status=400)

    #         product.model_name = data["model_name"] if 'model_name' in data else product.model_name
    #         product.description = data['description'] if 'description' in data else product.description
    #         product.capacity = data['capacity'] if 'capacity' in data else product.capacity
    #         product.sell_price = data['sell_price'] if 'sell_price' in data else product.sell_price
    #         product.cost_price = data['cost_price'] if 'cost_price' in data else product.cost_price
    #         product.save()
    #         return Response({"success": f"Saved changes in product {product.id}"}, status=200)

    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=400)
        temp_id = product.id
        product.delete()

        return Response({"success": f"deleted Product code {temp_id}"})