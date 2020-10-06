import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from aqa.users.models import User
from .models import Quotation, QuotationItem
from .serializers import (
    QuotationSerializer,
    QuotationItemSerializer
)


class QuotationListCreateView(ListCreateAPIView):
    model = Quotation
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

    def create(self, request):
        data = copy.deepcopy(request.data)
        user = User.objects.get(pk=request.user.id)
        data['author'] = user.id

        items_isvalid = [] # values are boolean True or False
        item_serializers = []

        if 'items' in data:
            for item in data['items']:
                item_serializer = QuotationItemSerializer(data=item)
                items_isvalid.append(item_serializer.is_valid())
                item_serializers.append(item_serializer)
        quotation_serializer = QuotationSerializer(data=data)

        if all(items_isvalid) and quotation_serializer.is_valid:
            quotation = quotation_serializer.save()
            for item_serializer in item_serializers:
                quotation_item = item_serializer.save()
                quotation_item.quotation = quotation
                quotation_item.save()
            quotation.save()
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        
        else: #check what data is invalid, and return the error
            all_isvalid = [quotation_serializer.is_valid()] + items_isvalid
            data_serializers = [item_serializers] + quotation_serializer
            for validity, serializer in zip(all_isvalid, data_serializers):
                if not validity:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error", "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

'''
class QuotationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Quotation
    queryset = Quotaion.objects.all()
    serializer_class = QuotationSerializer

    def retrieve(self, request, pk):
        if not Quotation.objects.filter(pk=pk).first():
            return Response({"error": f"Product code {pk} does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


    def update(self,request,pk):
        pass
'''

class QuotationFetchUpdateDestroyView(APIView):
    def get(self, request, quotation_pk):

        quotation = Quotation.objects.filter(pk=quotation_pk).first()

        if not quotation:
            context = {
                "error": f"Primary Key {quotation_pk} does not exists",
            }
            return Response(context, status=400)

        context = {
            "company_name": quotation.company_name,
            "id": quotation.id,
            "author": {"id": quotation.author.id, "username": quotation.author.username},
            #"expiry_date": quotation.expiry_date,
        }

        return Response(context, status=200)

    def put(self, request, quotation_pk):
            data = copy.deepcopy(request.data)
            quotation = Quotation.objects.filter(pk=quotation_pk).first()
            
            if not quotation:
                context = {
                    "error": f"Primary Key {quotation_pk} does not exists",
                }
                return Response(context, status=400)

            quotation.author = User.objects.filter(username=data["author"]).first() if 'author' in data else quotation.author
            quotation.expiry_date = data['expiry_date'] if 'expiry_date' in data else quotation.expiry_date
            quotation.company_name = data['company_name'] if 'company_name' in data else quotation.company_name
            quotation.save()
            return Response({"success": f"Saved {quotation.id}"}, status=200)

    def delete(self, request, quotation_pk):
        quotation = Quotation.objects.filter(pk=quotation_pk).first()
        
        if not quotation:
            context = {
                "error": f"Primary Key {quotation_pk} does not exists",
            }
            return Response(context, status=400)
        temp_id = quotation.id
        quotation.delete()

        return Response({"success": f"deleted quotatin id {temp_id}"})
    

class QuotationItemListCreateView(ListCreateAPIView):
    model = QuotationItem
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer

    def create(self, request):
        data = copy.deepcopy(request.data)
        serializer = QuotationItemSerializer(data=data)

        if serializer.is_valid():
            quotation_item = serializer.save()
            quotation_item.save()

            return Response(QuotationItemSerializer(quotation_item).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class QuotationItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = QuotationItem
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer


    def retrieve(self, request, quotation_item_pk):
        quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exists"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(QuotationItemSerializer(quotation_item).data, status=status.HTTP_200_OK)


    def update(self, request, quotation_item_pk):
        data = copy.deepcopy(request.data)
        quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exists"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = QuotationItemSerializer(quotation_item, data=data)

        if serializer.is_valid():
            quotation_item_obj = serializer.save()
            quotation_item_obj.save()
            return Response(QuotationItemSerializer(quotation_item_obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, quotation_item_pk):
        quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exists"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        temp_id, temp_quotation_id = quotation_item.id, quotation_item.quotation.id
        quotation_item.delete()

        return Response({"success": f"deleted quotation item {temp_id} - from quotation {temp_quotation_id}"})