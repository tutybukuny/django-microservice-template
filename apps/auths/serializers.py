from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(max_length=128, required=True)
    device_name = serializers.CharField(max_length=100, required=False)
