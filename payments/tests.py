from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment


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
            daily_fee=Decimal("2.00"),
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date.today() + timedelta(days=5),
        )

    @patch("payments.stripe_helper.reverse")
    @patch("payments.stripe_helper.stripe.checkout.Session.create")
    def test_create_stripe_session(self, mock_stripe, mock_reverse):
        """Test creating Stripe checkout session."""
        # Mock reverse to return dummy URLs
        mock_reverse.return_value = "/payments/success/"

        # Mock Stripe session response
        mock_session = MagicMock()
        mock_session.url = "https://checkout.stripe.com/session"
        mock_session.id = "cs_test_123"
        mock_stripe.return_value = mock_session

        from django.test import RequestFactory
        from payments.stripe_helper import create_stripe_session

        request = RequestFactory().get("/")

        payment = create_stripe_session(self.borrowing, request)

        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.borrowing, self.borrowing)
        self.assertEqual(payment.type, Payment.TYPE_PAYMENT)
        self.assertEqual(payment.status, Payment.STATUS_PENDING)
        self.assertEqual(payment.money_to_pay, Decimal("10.00"))  # 5 days * $2
        mock_stripe.assert_called_once()
