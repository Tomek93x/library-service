from django.core.management.base import BaseCommand

from notifications.tasks import schedule_overdue_check


class Command(BaseCommand):
    """Django command to set up scheduled tasks."""

    help = "Set up scheduled tasks for checking overdue borrowings"

    def handle(self, *args, **options):
        schedule_overdue_check()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully scheduled overdue borrowings check"
            )
        )
