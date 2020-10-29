import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Customer, Address, ContactPerson
from .serializers import CustomerSerializer, AddressSerializer, ContactPersonSerializer
from .pagination import CustomerPageNumberPagination


class CustomerListCreateView(ListCreateAPIView):
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomerPageNumberPagination

    def list(self, request):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        return super().list(request)


    def create(self, request):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        data = copy.deepcopy(request.data)
        serializer = CustomerSerializer(data=data)

        if serializer.is_valid():
            # check for duplicates
            if Customer.objects.filter(company=data['company']):
                content = {'error': f'Customer {data["company"]} already exists'}
                return Response(content, status=status.HTTP_404_BAD_REQUEST)

            customer = serializer.save()
            customer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


class CustomerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=pk)
            return Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {pk} does not exist'}, status=status.HTTP_404_BAD_REQUEST)


    def update(self, request, pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied
    
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {pk} does not exist'}, status=status.HTTP_404_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        serializer = CustomerSerializer(customer, data=data)

        if serializer.is_valid():
            # check for duplicate
            if Customer.objects.filter(company=data['company']).exclude(pk=pk):
                content = {'error': f'Customer {data["company"]} already exists'}
                return Response(content, status=status.HTTP_404_BAD_REQUEST)
            
            customer_obj = serializer.save()
            customer_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


    def destroy(self, request, pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {pk} does not exist'}, status=status.HTTP_404_BAD_REQUEST)

        temp_id, temp_company = customer.id, customer.company
        customer.delete()

        return Response({'success': f'deleted Customer {temp_id} - {temp_company}'}, status=status.HTTP_200_OK)


class CustomerQueryView(APIView):

    def get(self, request):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            query = request.query_params['query']
            if query:
                customer = Customer.objects.filter(company__icontains=query)
                serializer = CustomerSerializer(customer, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        
        except:
            return Response([], status=status.HTTP_200_OK)