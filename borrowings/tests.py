from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing


class BorrowingTests(TestCase):
    """Tests for Borrowing model and API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            inventory=5,
            daily_fee="2.00",
        )

    @patch("borrowings.views.create_stripe_session")
    @patch("borrowings.views.notify_new_borrowing")
    def test_create_borrowing(self, mock_notify, mock_stripe):
        """Test creating a borrowing."""
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowing-list")
        data = {
            "book": self.book.id,
            "expected_return_date": (date.today() + timedelta(days=7)).isoformat(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)
        mock_stripe.assert_called_once()
        mock_notify.assert_called_once()

    def test_list_borrowings_user_sees_own(self):
        """Test users see only their own borrowings."""
        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="testpass123"
        )
        Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date.today() + timedelta(days=7),
        )
        Borrowing.objects.create(
            book=self.book,
            user=other_user,
            expected_return_date=date.today() + timedelta(days=7),
        )

        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowing-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_borrowings_admin_sees_all(self):
        """Test admin sees all borrowings."""
        Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date.today() + timedelta(days=7),
        )
        Borrowing.objects.create(
            book=self.book,
            user=self.admin,
            expected_return_date=date.today() + timedelta(days=7),
        )

        self.client.force_authenticate(user=self.admin)
        url = reverse("borrowings:borrowing-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    @patch("borrowings.views.create_fine_payment")
    def test_return_book(self, mock_fine):
        """Test returning a book."""
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date.today() + timedelta(days=7),
        )
        self.book.inventory = 4
        self.book.save()

        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowing-return-book", args=[borrowing.id])
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.book.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 5)

    def test_cannot_borrow_out_of_stock(self):
        """Test cannot borrow when inventory is 0."""
        self.book.inventory = 0
        self.book.save()

        self.client.force_authenticate(user=self.user)
        url = reverse("borrowings:borrowing-list")
        data = {
            "book": self.book.id,
            "expected_return_date": (date.today() + timedelta(days=7)).isoformat(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
