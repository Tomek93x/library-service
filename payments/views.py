from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.stripe_helper import check_session_status


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for managing payments."""

    queryset = Payment.objects.select_related("borrowing__book", "borrowing__user")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Non-admin users see only their own payments."""
        queryset = self.queryset
        user = self.request.user

        if not user.is_staff:
            queryset = queryset.filter(borrowing__user=user)

        return queryset

    @action(detail=False, methods=["get"], url_path="success")
    def payment_success(self, request):
        """Handle successful payment and send Telegram notification."""
        from notifications.telegram_helper import notify_successful_payment

        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response(
                {"error": "Session ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment = Payment.objects.get(session_id=session_id)

            if check_session_status(session_id):
                payment.status = Payment.STATUS_PAID
                payment.save()

                # Send Telegram notification about successful payment
                notify_successful_payment(payment)

                return Response(
                    {"message": "Payment successful!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Payment not completed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"], url_path="cancel")
    def payment_cancel(self, request):
        """Handle cancelled payment."""
        return Response(
            {
                "message": "Payment cancelled. You can complete it later "
                           "(session expires in 24h)."
            },
            status=status.HTTP_200_OK,
        )
