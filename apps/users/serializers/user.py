from rest_framework import serializers

from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["deleted", "is_superuser", "password"]

    def validate_phone(self, phone):
        if self.instance and self.instance.phone == phone:
            return phone
        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(f"This phone {phone} is already existed")
        return phone

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserReadOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    fullname = serializers.CharField(read_only=True)
    ascii_name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    avatar_url = serializers.FileField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
