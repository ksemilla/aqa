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

    def list(self, request, *args, **kwargs):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        return super().list(request, *args, **kwargs)


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
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            customer = serializer.save()
            customer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, customer_pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
            return Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, customer_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied
    
        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        serializer = CustomerSerializer(customer, data=data)

        if serializer.is_valid():
            # check for duplicate
            if Customer.objects.filter(company=data['company']).exclude(pk=customer_pk):
                content = {'error': f'Customer {data["company"]} already exists'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
            customer_obj = serializer.save()
            customer_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, customer_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

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



class ContactPersonListCreateView(ListCreateAPIView):
    model = ContactPerson
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    pagination_class = CustomerPageNumberPagination

    def list(self, request, customer_pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        contact_persons = ContactPerson.objects.filter(customer=customer_pk)

        page = self.paginate_queryset(contact_persons)
        if page is not None:
            serializer = ContactPersonSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ContactPersonSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, customer_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        data['customer'] = customer_pk
        serializer = ContactPersonSerializer(data=data)

        if serializer.is_valid():
            # check for duplicates
            if data['name'] in ContactPerson.objects.filter(customer=customer_pk).values_list('name', flat=True):
                content = {'error': f'Contact Person {data["name"]} from {serializer.data.company} already exists'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            contact_person = serializer.save()
            contact_person.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactPersonRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = ContactPerson
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer

    def retrieve(self, request, customer_pk, contact_pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact_person = ContactPerson.objects.filter(customer=customer_pk).get(pk=contact_pk)
            return Response(ContactPersonSerializer(contact_person).data, status=status.HTTP_200_OK)
        except ContactPerson.DoesNotExist:
            content = {'error': f'Contact Person id {contact_pk} does not exist in {customer.company}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, customer_pk, contact_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied
    
        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact_person = ContactPerson.objects.filter(customer=customer_pk).get(pk=contact_pk)
        except ContactPerson.DoesNotExist:
            content = {'error': f'Contact Person id {contact_pk} does not exist in {customer.company}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        data['customer'] = customer_pk
        serializer = ContactPersonSerializer(contact_person, data=data)

        if serializer.is_valid():
            # check for duplicates
            if data['name'] in ContactPerson.objects.filter(customer=customer_pk).exclude(pk=contact_pk).values_list('name', flat=True):
                content = {'error': f'Contact Person {data["name"]} from {serializer.data.company} already exists'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            contact_person_obj = serializer.save()
            contact_person_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, customer_pk, contact_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact_person = ContactPerson.objects.filter(customer=customer_pk).get(pk=contact_pk)
        except ContactPerson.DoesNotExist:
            content = {'error': f'Contact Person id {contact_pk} does not exist in {customer.company}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        temp_name, temp_company = contact_person.name, contact_person.company
        contact_person.delete()

        return Response({'success': f'deleted Contact Person {temp_name} from {temp_company}'}, status=status.HTTP_200_OK)


class ContactPersonQueryView(APIView):

    def get(self, request):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            query = request.query_params['query']
            if query:
                contact_person = ContactPerson.objects.filter(name__icontains=query)
                serializer = ContactPersonSerializer(contact_person, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        
        except:
            return Response([], status=status.HTTP_200_OK)



class AddressListCreateView(ListCreateAPIView):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    pagination_class = CustomerPageNumberPagination

    def list(self, request, customer_pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        addresses = Address.objects.filter(customer=customer_pk)

        page = self.paginate_queryset(addresses)
        if page is not None:
            serializer = AddressSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AddressSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, customer_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        data['customer'] = customer_pk
        serializer = AddressSerializer(data=data)

        if serializer.is_valid():
            # check for duplicates
            if data['location'] in Address.objects.filter(customer=customer_pk).values_list('location', flat=True):
                content = {'error': f'Address {data["location"]} of {serializer.data.company} already exists'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            address = serializer.save()
            address.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def retrieve(self, request, customer_pk, address_pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.filter(customer=customer_pk).get(pk=address_pk)
            return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            content = {'error': f'Contact Person id {address_pk} does not exist in {customer.company}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, customer_pk, address_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied
    
        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.filter(customer=customer_pk).get(pk=address_pk)
        except Address.DoesNotExist:
            content = {'error': f'Contact Person id {address_pk} does not exist in {customer.company}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        data['customer'] = customer_pk
        serializer = AddressSerializer(address, data=data)

        if serializer.is_valid():
            # check for duplicates
            if data['location'] in Address.objects.filter(customer=customer_pk).exclude(pk=address_pk).values_list('location', flat=True):
                content = {'error': f'Address {data["location"]} from {serializer.data.company} already exists'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            address_obj = serializer.save()
            address_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, customer_pk, address_pk):
        # restricted_scope = ['user', 'scm']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Customer.DoesNotExist:
            return Response({'error': f'Customer id {customer_pk} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.filter(customer=customer_pk).get(pk=address_pk)
        except Address.DoesNotExist:
            content = {'error': f'Contact Person id {address_pk} does not exist in {customer.company}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        temp_location, temp_company = address.name, address.company
        address.delete()

        return Response({'success': f'deleted Address {temp_location} of {temp_company}'}, status=status.HTTP_200_OK)


class AddressQueryView(APIView):

    def get(self, request):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            query = request.query_params['query']
            if query:
                address = Address.objects.filter(location__icontains=query)
                serializer = ContactPersonSerializer(address, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        
        except:
            return Response([], status=status.HTTP_200_OK)