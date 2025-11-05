from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model."""

    list_display = [
        "id",
        "borrowing",
        "status",
        "type",
        "money_to_pay",
    ]
    list_filter = ["status", "type"]
    search_fields = ["borrowing__book__title", "borrowing__user__email"]
