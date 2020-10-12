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

        if all(items_isvalid) and quotation_serializer.is_valid():
            quotation = quotation_serializer.save()
            for item_serializer in item_serializers:
                quotation_item = item_serializer.save()
                quotation_item.quotation = quotation
                quotation_item.save()
            quotation.save()
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        
        else: #check what data is invalid, and return the error of that data
            all_isvalid = [quotation_serializer.is_valid()] + items_isvalid
            data_serializers = [quotation_serializer] + item_serializers
            for validity, serializer in zip(all_isvalid, data_serializers):
                if not validity:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error", "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class QuotationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Quotation
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

    def retrieve(self, request, quotation_pk):
        quotation = Quotation.objects.filter(pk=quotation_pk).first()
        if not quotation:
            return Response({"error": f"Quotation {quotation_pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)


    def update(self,request,quotation_pk):
        quotation = Quotation.objects.filter(pk=quotation_pk).first()
        if not quotation:
            return Response({"error": f"Quotation {quotation_pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        data = copy.deepcopy(request.data)
        user = User.objects.get(pk=request.user.id)
        data['author'] = user.id # the one who updated will be the new author

        items_isvalid = [] # values are boolean True or False
        item_serializers = []
        updated_ids = set()
        current_ids = set(quotation.quotationitem_set.all().values_list('pk', flat=True))

        if 'items' in data:
            for item in data['items']:
                if "id" in item:
                    quotation_item = quotation.quotationitem_set.filter(pk=item["id"]).first()
                    if not quotation_item:
                        content = {"error": f"Quotation item {item['id']} does not exist in Quotation {quotation.id}"}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)
                    item_serializer = QuotationItemSerializer(quotation_item, data=item)
                    updated_ids.add(item["id"])
                else:
                    item_serializer = QuotationItemSerializer(data=item)
                items_isvalid.append(item_serializer.is_valid())
                item_serializers.append(item_serializer)
        quotation_serializer = QuotationSerializer(quotation, data=data)

        if all(items_isvalid) and quotation_serializer.is_valid():
            #save the updated and created items and quotations in database
            quotation = quotation_serializer.save()
            quotation.save()
            for item_serializer in item_serializers:
                quotation_item = item_serializer.save()
                quotation_item.quotation = quotation
                quotation_item.save()

            #delete old items not in new data
            delete_ids = current_ids - updated_ids
            for item_id in delete_ids:
                quotation_item = quotation.quotationitem_set.get(id=item_id)
                quotation_item.delete()

            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)

        else: #check what data is invalid, and return the error of that data
            all_isvalid = [quotation_serializer.is_valid()] + items_isvalid
            data_serializers = [quotation_serializer] + item_serializers
            for validity, serializer in zip(all_isvalid, data_serializers):
                if not validity:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error", "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, quotation_pk):
        quotation = Quotation.objects.filter(pk=quotation_pk).first()
        if not quotation:
            return Response({"error": f"Quotation {quotation_pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
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
            content = {"error": f"Quotation item {quotation_item_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(QuotationItemSerializer(quotation_item).data, status=status.HTTP_200_OK)


    def update(self, request, quotation_item_pk):
        quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        data = copy.deepcopy(request.data)    
        serializer = QuotationItemSerializer(quotation_item, data=data)

        if serializer.is_valid():
            quotation_item_obj = serializer.save()
            quotation_item_obj.save()
            return Response(QuotationItemSerializer(quotation_item_obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, quotation_item_pk):
        quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        temp_id, temp_quotation_id = quotation_item.id, quotation_item.quotation.id
        quotation_item.delete()

        return Response({"success": f"deleted quotation item {temp_id} - from quotation {temp_quotation_id}"})