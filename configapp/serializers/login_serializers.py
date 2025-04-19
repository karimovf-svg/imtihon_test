from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import *

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "success": False,
                "message": "User does not exist"
            })

        auth_user = authenticate(phone_number=phone_number, password=password)
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "message": "Phone or password is invalid"
            })

        attrs['user'] = auth_user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password', 'email', 'is_active', 'is_staff', 'is_admin', 'is_teacher', 'is_student')
