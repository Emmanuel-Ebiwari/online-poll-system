from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

def register_user(data):
    serializer = UserRegistrationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    return {
        'user': serializer.data,
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

def login_user(data):
    serializer = UserLoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    identifier = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()

    if user is None:
        raise AuthenticationFailed("User not found")
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect password")
    if not user.is_active:
        raise AuthenticationFailed("User account is disabled")

    refresh = RefreshToken.for_user(user)
    return {
        'user': UserRegistrationSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
