from datetime import date

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for managing borrowings."""

    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter borrowings by user (non-admin see only their own)."""
        queryset = self.queryset
        user = self.request.user

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        user_id = self.request.query_params.get("user_id")
        if user_id and user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        """
        Create borrowing, attach user, decrease book inventory,
        create Stripe payment session, send Telegram notification.
        """
        from notifications.telegram_helper import notify_new_borrowing
        from payments.stripe_helper import create_stripe_session

        book = serializer.validated_data["book"]
        book.inventory -= 1
        book.save()

        borrowing = serializer.save(user=self.request.user)

        # Create Stripe payment session automatically
        create_stripe_session(borrowing, self.request)

        # Send Telegram notification about new borrowing
        notify_new_borrowing(borrowing)

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        """Return a borrowed book and create fine if overdue."""
        from payments.stripe_helper import create_fine_payment

        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"error": "Book already returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set actual return date (from request or today)
        actual_date = request.data.get("actual_return_date")
        if actual_date:
            borrowing.actual_return_date = actual_date
        else:
            borrowing.actual_return_date = date.today()

        # Increase book inventory
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        # Create fine payment if book is returned late
        if borrowing.actual_return_date > borrowing.expected_return_date:
            create_fine_payment(borrowing, request)

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)
