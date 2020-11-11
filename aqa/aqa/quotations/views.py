import copy
import json

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny

from aqa.users.models import User
from .models import Quotation, QuotationItem
from .serializers import QuotationSerializer, QuotationItemSerializer, CreateQuotationItemSerializer
from .pagination import QuotationItemPageNumberPagination, QuotationPageNumberPagination
from .const import QuotationDays


class QuotationListCreateView(ListCreateAPIView):
    model = Quotation
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]
    pagination_class = QuotationPageNumberPagination


    def list(self, request, *args, **kwargs):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        return super().list(request, *args, **kwargs)


    def create(self, request):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        data = copy.deepcopy(request.data)
        user = User.objects.get(pk=request.user.id)
        data['author'] = user.id

        items_isvalid = [] # values are boolean True or False
        item_serializers = []

        quotation_serializer = QuotationSerializer(data=data)
        if 'items' in data:
            for item in data['items']:
                item_serializer = CreateQuotationItemSerializer(data=item)
                items_isvalid.append(item_serializer.is_valid())
                item_serializers.append(item_serializer)

        if all(items_isvalid) and quotation_serializer.is_valid():
            quotation = quotation_serializer.save(last_modified=None)
            for item_serializer in item_serializers:
                quotation_item = item_serializer.save(quotation=quotation)
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

        try:
            quotation = Quotation.objects.get(pk=quotation_pk)
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        except Quotation.DoesNotExist:
            content = {"error": f"Quotation {quotation_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, quotation_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        # retrieve the quotation
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
        data['author'] = quotation.author.id # the author will never change

        items_isvalid = [] # values are boolean True or False
        item_serializers = []

        updated_ids = set()
        current_ids = set(quotation.quotationitem_set.all().values_list('pk', flat=True))

        # get the serializers and validity of quotation items
        if 'items' in data:
            for item in data['items']:

                if "id" in item: # if id is in data, this id will be overwritten
                    try:
                        quotation_item = quotation.quotationitem_set.get(pk=item["id"])
                    except QuotationItem.DoesNotExist:
                        content = {"error": f"Quotation item {item['id']} does not exist in Quotation {quotation.id}"}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)
                    item['quotation'] = quotation_pk
                    item_serializer = QuotationItemSerializer(quotation_item, data=item)
                    updated_ids.add(item["id"])
    
                else: # if no id is provided, then this is a new quotation_item
                    item['quotation'] = quotation_pk
                    item_serializer = QuotationItemSerializer(data=item)
    
                items_isvalid.append(item_serializer.is_valid())
                item_serializers.append(item_serializer)
        quotation_serializer = QuotationSerializer(quotation, data=data)


        if all(items_isvalid) and quotation_serializer.is_valid():

            #save the updated and created items and quotations in database
            quotation = quotation_serializer.save(last_modified=user)
            for item_serializer in item_serializers:
                quotation_item = item_serializer.save()
                quotation_item.save()
            quotation.save()
            
            # delete old items not in new data
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



class QuotationReminderView(ListAPIView):
    model = Quotation
    queryset = Quotation.objects.exclude(
        expiry_date__lte=timezone.now()
    ).filter(
        expiry_date__lte=timezone.now()+timezone.timedelta(days=QuotationDays.QUOTE_REMINDER))
    serializer_class = QuotationSerializer
    pagination_class = QuotationPageNumberPagination
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]
    
    def list(self, request, *args, **kwargs):
        # if request.user not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        return super().list(request, *args, **kwargs)



class QuotationItemListCreateView(ListCreateAPIView):
    model = QuotationItem
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer
    allowed_scope = ['ae', 'se', 'sl', 'bh', 'admin',]
    pagination_class = QuotationItemPageNumberPagination


    def list(self, request, *args, **kwargs):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        return super().list(request, *args, **kwargs)


    def create(self, request):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        data = copy.deepcopy(request.data)
        serializer = QuotationItemSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # check if the user has access to the data['quotation']
        if request.user.scope == 'ae':
            quotation = request.user.quotations_as_ae.filter(pk=data['quotation']).first()
        elif request.user.scope == 'se':
            quotation = request.user.quotations_as_se.filter(pk=data['quotation']).first()
        elif request.user.scope == 'sl':
            quotation = request.user.quotations_as_sl.filter(pk=data['quotation']).first()
        else:
            quotation = Quotation.objects.filter(pk=data['quotation']).first()

        if not quotation:
            content = {"error": f"Quotation {data['quotation']} does not exist or cannot be accessed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


        if serializer.is_valid():
            quotation_item = serializer.save()
            quotation_item.save()
            quotation.last_modified = request.user
            quotation.save()
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

        try:
            quotation_item = QuotationItem.objects.get(pk=quotation_item_pk)
            return Response(QuotationItemSerializer(quotation_item).data, status=status.HTTP_200_OK)
        except QuotationItem.DoesNotExist:
            content = {"error": f"Quotation item {quotation_item_pk} does not exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, quotation_item_pk):
        # if request.user.scope not in self.allowed_scope:
        #     raise exceptions.PermissionDenied

        # check if the quotationitem is within the quotation in which the user has access to for certain scope
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
        data['quotation'] = quotation_item.quotation.id
        quotation = quotation_item.quotation
        serializer = QuotationItemSerializer(quotation_item, data=data)

        if serializer.is_valid():
            quotation_item_obj = serializer.save()
            quotation.last_modified = request.user
            quotation.save()
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