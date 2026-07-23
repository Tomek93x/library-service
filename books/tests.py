from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book


class BookTests(TestCase):
    """Tests for Book model and API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 10,
            "daily_fee": "1.50",
        }
        self.book = Book.objects.create(**self.book_data)

    def test_list_books_unauthenticated(self):
        """Test listing books without authentication."""
        url = reverse("books:book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_as_admin(self):
        """Test creating book as admin."""
        self.client.force_authenticate(user=self.admin)
        url = reverse("books:book-list")
        response = self.client.post(url, self.book_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.book_data["title"])

    def test_create_book_as_user_forbidden(self):
        """Test regular user cannot create books."""
        self.client.force_authenticate(user=self.user)
        url = reverse("books:book-list")
        response = self.client.post(url, self.book_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_admin(self):
        """Test updating book as admin."""
        self.client.force_authenticate(user=self.admin)
        url = reverse("books:book-detail", args=[self.book.id])
        updated_data = {"title": "Updated Title"}
        response = self.client.patch(url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")
