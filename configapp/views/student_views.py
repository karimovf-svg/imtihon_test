from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..make_token import *
from ..serializers import *
from ..add_permission import *

class StudentCreate(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    def get(self, request):
        data = {'success': True}
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        data['student'] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def post(self, request):
        data = {'success': True}
        user = request.data['user']
        student = request.data['student']
        phone_number = user['phone_number']
        user_serializer = UserSerializer(data=user)
        user['is_student'] = True
        user['is_active'] = True

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.password = (make_password(user_serializer.validated_data.get('password')))
            user = user_serializer.save()
            user_id = User.objects.filter(phone_number=phone_number).values('id')[0]['id']
            student['user'] = user_id
            student_serializer = StudentSerializer(data=student)
            if student_serializer.is_valid(raise_exception=True):
                student_serializer.save()
                data['user'] = user_serializer.data
                data['student'] = student_serializer.data
                return Response(data=data)
            return Response(data=student_serializer.errors)
        return Response(data=user_serializer.errors)

class StudentUpdateView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk)

    @swagger_auto_schema(request_body=StudentSerializer)
    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

