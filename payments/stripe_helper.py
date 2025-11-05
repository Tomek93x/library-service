from decimal import Decimal

import stripe
from django.conf import settings
from django.urls import reverse

from payments.models import Payment


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(borrowing, request):
    """Create Stripe checkout session for borrowing."""

    # Calculate total price (days * daily_fee)
    days = (borrowing.expected_return_date - borrowing.borrow_date).days
    if days < 1:
        days = 1

    # Convert days to Decimal and multiply by daily_fee
    total_price = Decimal(days) * borrowing.book.daily_fee

    # Convert to cents for Stripe
    unit_amount = int(total_price * 100)

    # Build success and cancel URLs
    success_url = request.build_absolute_uri(
        reverse("payments:payment-success")
    )
    cancel_url = request.build_absolute_uri(
        reverse("payments:payment-cancel")
    )

    # Create Stripe session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Borrowing: {borrowing.book.title}",
                        "description": f"Book rental for {days} days",
                    },
                    "unit_amount": unit_amount,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
    )

    # Create Payment record
    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=total_price,
        type=Payment.TYPE_PAYMENT,
        status=Payment.STATUS_PENDING,
    )

    return payment


def create_fine_payment(borrowing, request):
    """Create fine payment for overdue borrowing."""

    # Calculate overdue days
    overdue_days = (
        borrowing.actual_return_date - borrowing.expected_return_date
    ).days
    if overdue_days <= 0:
        return None

    # Calculate fine amount - convert all to Decimal
    fine_amount = (
        Decimal(overdue_days)
        * borrowing.book.daily_fee
        * Decimal(settings.FINE_MULTIPLIER)
    )

    # Convert to cents for Stripe
    unit_amount = int(fine_amount * 100)

    # Build URLs
    success_url = request.build_absolute_uri(
        reverse("payments:payment-success")
    )
    cancel_url = request.build_absolute_uri(
        reverse("payments:payment-cancel")
    )

    # Create Stripe session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"FINE: {borrowing.book.title}",
                        "description": f"Overdue fine for {overdue_days} days",
                    },
                    "unit_amount": unit_amount,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
    )

    # Create Payment record
    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=fine_amount,
        type=Payment.TYPE_FINE,
        status=Payment.STATUS_PENDING,
    )

    return payment


def check_session_status(session_id):
    """Check Stripe session payment status."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session.payment_status == "paid"
