from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment
from payments.stripe_helper import create_stripe_session


class PaymentTests(TestCase):
    """Tests for Payment model and Stripe integration."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="SOFT",
            inventory=5,
            daily_fee="2.00",
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date.today() + timedelta(days=5),
        )

    @patch("payments.stripe_helper.stripe.checkout.Session.create")
    def test_create_stripe_session(self, mock_stripe):
        """Test creating Stripe checkout session."""
        mock_stripe.return_value.url = "https://checkout.stripe.com/session"
        mock_stripe.return_value.id = "cs_test_123"

        from django.test import RequestFactory

        request = RequestFactory().get("/")
        payment = create_stripe_session(self.borrowing, request)

        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.borrowing, self.borrowing)
        self.assertEqual(payment.type, Payment.TYPE_PAYMENT)
        self.assertEqual(payment.status, Payment.STATUS_PENDING)
        mock_stripe.assert_called_once()
