from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserDetailSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view with proper header name."""

    pass
