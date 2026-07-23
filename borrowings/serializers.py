from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    """Serializer for Borrowing model."""

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]
        read_only_fields = ["id", "borrow_date", "user"]


class BorrowingDetailSerializer(BorrowingSerializer):
    """Detailed serializer with nested book info and payments."""

    book = BookSerializer(read_only=True)
    payments = serializers.SerializerMethodField()

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + ["payments"]

    def get_payments(self, obj):
        """Return all payments for this borrowing."""
        from payments.serializers import PaymentSerializer

        payments = obj.payments.all()
        return PaymentSerializer(payments, many=True).data


class BorrowingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating borrowings."""

    class Meta:
        model = Borrowing
        fields = ["id", "expected_return_date", "book"]
        read_only_fields = ["id"]

    def validate_book(self, value):
        """Validate that book has available inventory."""
        if value.inventory < 1:
            raise serializers.ValidationError(
                "This book is currently out of stock."
            )
        return value
