from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name')
