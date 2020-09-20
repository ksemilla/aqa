import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from aqa.users.models import User
from .models import Quotation

class QuotationSampleView(APIView):
    def get(self, request):

        quotations = Quotation.objects.all()

        lists = []
        for quotation in quotations:
            lists.append(
                {
                    "company_name":quotation.company_name,
                    "id": quotation.id,
                    "author": {"id": quotation.author.id, "username": quotation.author.username},
                    "expiry_date": quotation.expiry_date,
                }
            )

        return Response(lists, status=200)

    def post(self, request):
        data = copy.deepcopy(request.data)

        author = User.objects.filter(username=data["author"]).first()

        # Error Handling
        if not author:
            return Response({"error": "Something went wrong :("}, status=400)

        required_fields = {"company_name", "author"}
        # if any(field not in data for field in required_fields):
        missing_info = []
        for field in required_fields:
            if field not in data:
                missing_info.append(field)
        if missing_info:
            return Response({"error": f"Incomplete data. Please input: {missing_info}"}, status=400)


        created_quotation = Quotation.objects.create(
            company_name=data["company_name"] if "company_name" in data else "",
            author=User.objects.filter(username=data["author"]).first(),
        )

        context = {
            "success": f"Created quotation id {created_quotation.id} for {created_quotation.company_name}"
        }

        return Response(context, status=200)


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
            "expiry_date": quotation.expiry_date,
        }

        print(context)

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
            print(quotation.author)
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