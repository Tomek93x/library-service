from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserTests(TestCase):
    """Tests for User model and API."""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user(self):
        """Test creating a new user."""
        url = reverse("users:register")
        response = self.client.post(url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_token_generation(self):
        """Test JWT token generation."""
        user = get_user_model().objects.create_user(**self.user_data)
        url = reverse("users:token")
        response = self.client.post(
            url, {"email": user.email, "password": self.user_data["password"]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_retrieve_user_profile(self):
        """Test retrieving authenticated user profile."""
        user = get_user_model().objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        url = reverse("users:me")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
