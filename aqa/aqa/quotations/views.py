import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
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
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]


    def list(self, request):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        print(request.query_params)
        print(243234)

        serializer = QuotationSerializer(Quotation.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

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
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]

    def retrieve(self, request, quotation_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        quotation = Quotation.objects.filter(pk=quotation_pk).first()
        if not quotation:
            content = {"error": f"Quotation {quotation_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)


    def update(self,request,quotation_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        if request.user.scope == 'ae':
            quotation = request.user.quotations_as_ae.filter(pk=quotation_pk).first()
        elif request.user.scope == 'se':
            quotation = request.user.quotations_as_se.filter(pk=quotation_pk).first()
        elif request.user.scope == 'sl':
            quotation = request.user.quotations_as_sl.filter(pk=quotation_pk).first()
        else:
            quotation = Quotation.objects.filter(pk=quotation_pk).first()

        if not quotation:
            content = {"error": f"Quotation {quotation_pk} does not exist or cannot be accessed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
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


    def destroy(self, request, quotation_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        if request.user.scope == 'ae':
            quotation = request.user.quotations_as_ae.filter(pk=quotation_pk).first()
        elif request.user.scope == 'se':
            quotation = request.user.quotations_as_se.filter(pk=quotation_pk).first()
        elif request.user.scope == 'sl':
            quotation = request.user.quotations_as_sl.filter(pk=quotation_pk).first()
        else:
            quotation = Quotation.objects.filter(pk=quotation_pk).first()

        if not quotation:
            content = {"error": f"Quotation {quotation_pk} does not exist or cannot be accessed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        temp_id = quotation.id
        quotation.delete()
        return Response({"success": f"Deleted Quotation {temp_id}"})



class QuotationItemListCreateView(ListCreateAPIView):
    model = QuotationItem
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]

    def list(self, request):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        serializer = QuotationItemSerializer(QuotationItem.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

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
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]

    def retrieve(self, request, quotation_item_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(QuotationItemSerializer(quotation_item).data, status=status.HTTP_200_OK)


    def update(self, request, quotation_item_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        if request.user.scope == 'ae':
            quotation_item = QuotationItem.objects.filter(quotation__application_engr=request.user.id).filter(pk=quotation_item_pk).first()
        elif request.user.scope == 'se':
            quotation_item = QuotationItem.objects.filter(quotation__sales_engr=request.user.id).filter(pk=quotation_item_pk).first()
        elif request.user.scope == 'sl':
            quotation_item = QuotationItem.objects.filter(quotation__sales_lead=request.user.id).filter(pk=quotation_item_pk).first()
        else:
            quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()
        
        # check if quotation_item is existing or can be accessed
        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exist or cannot be accessed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        data = copy.deepcopy(request.data) 
        
        # quotation should NOT be modified
        if ('quotation' in data) and (data['quotation'] != quotation_item.quotation.id):
            content = {"error": "Invalid request. Quotation ID cannot be changed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer = QuotationItemSerializer(quotation_item, data=data)

        if serializer.is_valid():
            quotation_item_obj = serializer.save()
            quotation_item_obj.save()
            return Response(QuotationItemSerializer(quotation_item_obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, quotation_item_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        if request.user.scope == 'ae':
            quotation_item = QuotationItem.objects.filter(quotation__application_engr=request.user.id).filter(pk=quotation_item_pk).first()
        elif request.user.scope == 'se':
            quotation_item = QuotationItem.objects.filter(quotation__sales_engr=request.user.id).filter(pk=quotation_item_pk).first()
        elif request.user.scope == 'sl':
            quotation_item = QuotationItem.objects.filter(quotation__sales_lead=request.user.id).filter(pk=quotation_item_pk).first()
        else:
            quotation_item = QuotationItem.objects.filter(pk=quotation_item_pk).first()


        if not quotation_item:
            content = {"error": f"Quotation item {quotation_item_pk} does not exist or cannot be accessed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        temp_id, temp_quotation_id = quotation_item.id, quotation_item.quotation.id
        quotation_item.delete()

        return Response({"success": f"deleted quotation item {temp_id} - from quotation {temp_quotation_id}"})