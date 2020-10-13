import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(ListCreateAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        restricted_scope = ['user']
        if request.user.scope in restricted_scope:
            raise exceptions.PermissionDenied
        
        serializer = ProductSerializer(Product.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        allowed_scope = ['admin', 'scm']
        if request.user.scope not in allowed_scope:
            raise exceptions.PermissionDenied
       
        data = copy.deepcopy(request.data)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            # Check for duplicates. A duplicate product has the same 
            # description and model_name with an existing product
            if Product.objects.filter(model_name=data["model_name"]).filter(description=data["description"]):
                content = {"error": f"Product {data['model_name']} - {data['description']} already exists"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            product = serializer.save()
            product.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def retrieve(self, request, pk):
        restricted_scope = ['user']
        if request.user.scope in restricted_scope:
            raise exceptions.PermissionDenied

        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        
    
    def update(self, request, pk):
        allowed_scope = ['admin', 'scm']
        if request.user.scope not in allowed_scope:
            raise exceptions.PermissionDenied
       
        data = copy.deepcopy(request.data)
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():

            #Check for duplicates. A duplicate has the same description and model name with existing product
            if ('model_name' in data) and ('description' in data):
                if Product.objects.filter(model_name=data["model_name"]).filter(description=data["description"]).exclude(pk=pk):
                    content = {"error": f"Product {data['model_name']} - {data['description']} already exists"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            product_obj = serializer.save()
            product_obj.save()
            return Response(ProductSerializer(product_obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        allowed_scope = ['admin', 'scm']
        if request.user.scope not in allowed_scope:
            raise exceptions.PermissionDenied

        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"error": f"Product code {pk} does not exist"}, status=400)
        temp_id, temp_model_name = product.id, product.model_name
        product.delete()

        return Response({"success": f"deleted Product code {temp_id} - {temp_model_name}"})