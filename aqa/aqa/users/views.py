from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
#from django.views.generic import DetailView, RedirectView, UpdateView, ListAPIView, UpdateAPIView

import copy
import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

User = get_user_model()

class UserListView(ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        permission_scope = ['admin', 'bh']
        if request.user.scope not in permission_scope:
            return Response({'error':'Access denied'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateView(CreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = copy.deepcopy(request.data)
        if User.objects.filter(username=data["username"]).exists(): # check if username already exists
            content = {
                "error": f"Error: Username {data['username']} already exists."
            }
            return Response(content, status=400)

        new_user = User.objects.create(
            username=data["username"],
            email=data["email"]
        )
        new_user.set_password(data["password"])
        new_user.save()

        content = {
            "success": f"New user {new_user.username} successfully created"
        }
        return Response(content, status=status.HTTP_200_OK)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    pass


# class UserDetailView(LoginRequiredMixin, DetailView):

#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"

# #-----django original code-----#
# user_detail_view = UserDetailView.as_view()


# class UserUpdateView(LoginRequiredMixin, UpdateView):

#     model = User
#     fields = ["name"]

#     def get_success_url(self):
#         return reverse("users:detail", kwargs={"username": self.request.user.username})

#     def get_object(self):
#         return User.objects.get(username=self.request.user.username)

#     def form_valid(self, form):
#         messages.add_message(
#             self.request, messages.INFO, _("Infos successfully updated")
#         )
#         return super().form_valid(form)


# user_update_view = UserUpdateView.as_view()


# class UserRedirectView(LoginRequiredMixin, RedirectView):

#     permanent = False

#     def get_redirect_url(self):
#         return reverse("users:detail", kwargs={"username": self.request.user.username})


# user_redirect_view = UserRedirectView.as_view()
# #-----django original code-----#