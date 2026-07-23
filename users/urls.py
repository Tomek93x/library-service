from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    CreateUserView,
    CustomTokenObtainPairView,
    ManageUserView,
)


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", ManageUserView.as_view(), name="me"),
]

app_name = "users"
