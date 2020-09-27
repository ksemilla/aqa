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
        
    
    # def update(self, request, pk):
    #     data = copy.deepcopy(request.data)
    #     product = Product.objects.filter(pk=pk).first()
    #     if not product:
    #         return Response({"error": f"Product code {pk} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    #     serializer = ProductSerializer(data=data)
    #     if serializer.is_valid():
    #         for attr, value in data.items():
    #             setattr(product, attr, value)
    #             product.save()
    #     return Response({"success": f"Saved changes in product {product.model_name}", "new_data": ProductSerializer(product).data}, status=status.HTTP_200_OK)

    def update(self, request, pk):
        data = copy.deepcopy(request.data)
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(product, data=data)

        if serializer.is_valid():
            product_obj = serializer.save()
            return Response(ProductSerializer(product_obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=400)
        temp_id = product.id
        product.delete()

        return Response({"success": f"deleted Product code {temp_id}"})