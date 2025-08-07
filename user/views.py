from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import User
from .serializers import UserSerializer
from .services import login_user, register_user


class UserViewSet(viewsets.ModelViewSet):
    """
    Handles user authentication-related endpoints
    like login and registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Default for /users/
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return User.objects.all()
    #     return User.objects.filter(pk=user.pk)  # Only see yourself
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        # Non-admin users only get themselves
        return User.objects.filter(pk=user.pk)

    def get_object(self):
        obj = super().get_object()

        if self.request.user.is_superuser or obj == self.request.user:
            return obj

        raise PermissionDenied("You do not have permission to view this user.")
    
    def get_serializer(self, *args, **kwargs):
        # Prevent browsable API from showing update/delete form
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            try:
                self.get_object()  # Force permission check and 404 here
            except (PermissionDenied, NotFound):
                return None  # Returning None disables form rendering
        return super().get_serializer(*args, **kwargs)

    def _check_permission(self):
        obj = self.get_object()
        if not self.request.user.is_superuser and obj != self.request.user:
            raise PermissionDenied("You do not have permission to modify this user.")

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only admins can list all users.")
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._check_permission()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_permission()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_permission()
        return super().destroy(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        # Disables default user creation via POST to /users/.
        # (User creation is handled via the /users/register/ route.)
        return Response({'detail': 'Method POST not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'], url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        """
        Custom endpoint for new user registration.
        Saves a new user and returns authentication tokens (access & refresh).
        """
        data = register_user(request.data)
        return Response(data, status=201)

    @action(detail=False, methods=['post'], url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        """
        Authenticates a user by either username or email.
        Returns JWT access and refresh tokens upon successful login.
        """
        data = login_user(request.data)
        return Response(data, status=200)