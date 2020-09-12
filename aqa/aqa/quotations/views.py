import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Quotation

class QuotationSampleView(APIView):
    def get(self, request):

        quotations = Quotation.objects.all()

        lists = []
        for quotation in quotations:
            lists.append(
                {
                    "id": quotation.id,
                    "author": quotation.author,
                    "expiry_date": quotation.expiry_date,
                }
            )

        return Response(lists, status=200)

    def post(self, request):
        data = copy.deepcopy(request.data)

        print(data)

        # check is author already exists

        data_to_check = Quotation.objects.filter(
            author=data["author"]
        )

        if len(data_to_check) > 0:

            context = {
                "error": f"Author {data['author']} already exists"
            }

            return Response(context, status=400)

        created_quotation = Quotation.objects.create(
            author=data["author"],
            expiry_date = data["expiry_date"]
        )

        context = {
            "success": f"Created quotation id {created_quotation.id} with author {created_quotation.author}"
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
            "id": quotation.id,
            "author": quotation.author
        }

        print(context)

        return Response(context, status=200)

    def delete(self, request, pk):
        quotation = Quotation.objects.get(pk=pk)
        quotation.delete()

        return Response({"success": f"deleted {quotation.id}"})