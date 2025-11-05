from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    """Model representing a payment for borrowing."""

    STATUS_PENDING = "PENDING"
    STATUS_PAID = "PAID"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
    ]

    TYPE_PAYMENT = "PAYMENT"
    TYPE_FINE = "FINE"

    TYPE_CHOICES = [
        (TYPE_PAYMENT, "Payment"),
        (TYPE_FINE, "Fine"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=TYPE_PAYMENT
    )
    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
