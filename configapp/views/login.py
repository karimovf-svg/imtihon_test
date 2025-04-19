from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..make_token import *
from ..serializers import *


class LoginApi(APIView):
    permission_classes = [AllowAny,]
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token = get_tokens_for_user(user)
        token['is_admin'] = user.is_admin
        return Response(data=token, status=status.HTTP_200_OK)

class RegisterUserApi(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response({
                    'status': True,
                    'detail': 'CREATE'
            })

    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)


class UserDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)