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

            #Check for duplicates. A duplicate has the same description and model name with existing product
            if Product.objects.filter(model_name=data["model_name"]).filter(description=data["description"]):
                return Response({"error": f"Product {data['model_name']} - {data['description']} is already existing"}, status=status.HTTP_400_BAD_REQUEST)

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
        
        serializer = ProductSerializer(product, data=data)

        if serializer.is_valid():
            product_obj = serializer.save()
            return Response(ProductSerializer(product_obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        
        if not product:
            return Response({"error": f"Product code {pk} does not exists"}, status=400)
        temp_id, temp_model_name = product.id, product.model_name
        product.delete()

        return Response({"success": f"deleted Product code {temp_id} - {temp_model_name}"})