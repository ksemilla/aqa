import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from aqa.users.models import User
from .models import Quotation
from .serializers import (
    QuotationSerializer,
    QuotationItemSerializer
)


class QuotationListCreateView(ListCreateAPIView):
    model = Quotation
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

    # def create(self, request):
    #     data = copy.deepcopy(request.data)
    #     author = User.objects.get(pk=pk)
    #     data["author"] = author.id

    #     data_is_valid = []
    #     item_serializers = []

    #     if "items" in data:
    #         for item in data["items"]:
    #             item_serializer = QuotationItemSerializer(item)
    #             data_is_valid.append(item_serializer.is_valid())
    #             item_serializers.append(item_serializer)
            
    #     quotation_serializer = QuotationSerializer(data=data)
    #     data_is_valid.append(quotation_serializer.is_valid())
                
    #     if all(data_is_valid):
    #         quotation = serializer.save()
    #         quotation.save()

    #         return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
    #     return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        























    def create(self, request):
        data = copy.deepcopy(request.data)
        user = User.objects.get(pk=request.user.id)
        data['author'] = user.id

        serializers_list = [] # values are boolean True or False
        serializer_container = []

        if 'items' in data:
            for item in data['items']:
                serializer = QuotationItemSerializer(data=item)
                serializers_list.append(serializer.is_valid())
                serializer_container.append(serializer)

        serializer = QuotationSerializer(data=data)
        serializers_list.append(serializer.is_valid())

        if all(serializers_list):
            quotation = serializer.save()

            for item_serializer in serializer_container:
                quotation_item = item_serializer.save()
                quotation_item.quotation = quotation
                quotation_item.save()

            quotation.save()
            print(data)
            return Response(QuotationSerializer(quotation).data, status=status.HTTP_200_OK)
        return Response({"error", "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class QuotationFetchUpdateDestroy(APIView):
    def get(self, request, pk):

        quotation = Quotation.objects.filter(pk=pk).first()

        if not quotation:
            context = {
                "error": f"Primary Key {pk} does not exists",
            }
            return Response(context, status=400)

        context = {
            "company_name": quotation.company_name,
            "id": quotation.id,
            "author": {"id": quotation.author.id, "username": quotation.author.username},
            #"expiry_date": quotation.expiry_date,
        }

        return Response(context, status=200)

    def put(self, request, pk):
            data = copy.deepcopy(request.data)
            quotation = Quotation.objects.filter(pk=pk).first()
            
            if not quotation:
                context = {
                    "error": f"Primary Key {pk} does not exists",
                }
                return Response(context, status=400)

            quotation.author = User.objects.filter(username=data["author"]).first() if 'author' in data else quotation.author
            quotation.expiry_date = data['expiry_date'] if 'expiry_date' in data else quotation.expiry_date
            quotation.company_name = data['company_name'] if 'company_name' in data else quotation.company_name
            quotation.save()
            return Response({"success": f"Saved {quotation.id}"}, status=200)

    def delete(self, request, pk):
        quotation = Quotation.objects.filter(pk=pk).first()
        
        if not quotation:
            context = {
                "error": f"Primary Key {pk} does not exists",
            }
            return Response(context, status=400)
        temp_id = quotation.id
        quotation.delete()

        return Response({"success": f"deleted quotatin id {temp_id}"})