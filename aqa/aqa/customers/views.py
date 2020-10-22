import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Customer
# from .serializers import CustomerSerializer

class CustomerListCreateView(ListCreateAPIView):
    pass
    # return Response({}, status=status.HTTP_200_OK)