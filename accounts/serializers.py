from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password",)
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Bu email bilan ro'yxatdan o'tilgan")
        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if user is None:
            raise serializers.ValidationError("Email yoki parol noto'g'ri")
        return {"user": user}