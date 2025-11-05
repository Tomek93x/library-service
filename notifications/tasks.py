from datetime import date

from django_q.tasks import schedule

from borrowings.models import Borrowing
from notifications.telegram_helper import (
    notify_overdue_borrowing,
    send_telegram_message,
)


def check_overdue_borrowings():
    """Check for overdue borrowings and send notifications."""
    today = date.today()

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=today,
        actual_return_date__isnull=True
    ).select_related("book", "user")

    if not overdue_borrowings.exists():
        send_telegram_message("✅ No borrowings overdue today!")
        return

    for borrowing in overdue_borrowings:
        notify_overdue_borrowing(borrowing)


def schedule_overdue_check():
    """Schedule daily task to check overdue borrowings."""
    schedule(
        "notifications.tasks.check_overdue_borrowings",
        schedule_type="daily",
        repeats=-1,  # Repeat indefinitely
    )
