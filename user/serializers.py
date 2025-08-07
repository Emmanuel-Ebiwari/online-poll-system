from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes full user data including admin fields.
    Used for listing or retrieving user profiles.
    """
    # password is write-only to prevent exposure in API responses.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_superuser', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Used for registering new users with minimal required fields.
    """
    # password is write-only to prevent exposure in API responses.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Creates a new user with a hashed password using Django’s create_user() method.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Handles user login input validation using username/email and password.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) # password is write-only to prevent exposure in API responses.