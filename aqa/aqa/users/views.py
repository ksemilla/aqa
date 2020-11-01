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
from rest_framework import status, exceptions

from .serializers import UserSerializer
from .pagination import UserPageNumberPagination

User = get_user_model()

class UserListView(ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPageNumberPagination

    def list(self, request):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        return super().list(request)


class UserCreateView(CreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        data = copy.deepcopy(request.data)
        serializer = UserSerializer(data=data)

        if serializer.is_valid():                
            new_user = serializer.save()
            new_user.set_password(data["password"])
            new_user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def retrieve(self, request, user_pk):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        try:
            user = User.objects.get(pk=user_pk)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"User id {user_pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, user_pk):
        # allowed_scope = ['admin']
        # if (request.user.scope not in allowed_scope) and (request.user.id != user_pk):
        #     raise exceptions.PermissionDenied

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"error": f"User id {user_pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        data = copy.deepcopy(request.data)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():

            #Check for duplicate email
            if 'email' in data:
                if User.objects.filter(email=data["email"]).exclude(pk=user_pk):
                    content = {"error": f"email {data['email']} already exists"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            if 'password' in data:
                user.set_password(data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, user_pk):
        # allowed_scope = ['admin']
        # if request.user.scope not in allowed_scope:
        #     raise exceptions.PermissionDenied

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({"error": f"User id {user_pk} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        temp_id, temp_username = user.id, user.username
        user.delete()

        return Response({"success": f"deleted user {temp_id} - {temp_username}"}, status=status.HTTP_200_OK)


class RoleListView(ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        # restricted_scope = ['user']
        # if request.user.scope in restricted_scope:
        #     raise exceptions.PermissionDenied

        role_list = {}
        ae_list = UserSerializer(User.objects.filter(scope='ae'), many=True).data
        se_list = UserSerializer(User.objects.filter(scope='se'), many=True).data
        sl_list = UserSerializer(User.objects.filter(scope='sl'), many=True).data
        role_list['ae'] = list(ae_list)
        role_list['se'] = list(se_list)
        role_list['sl'] = list(sl_list)

        return Response(role_list, status=status.HTTP_200_OK)


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