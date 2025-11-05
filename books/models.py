from django.db import models


class Book(models.Model):
    """Model representing a book in the library."""

    COVER_HARD = "HARD"
    COVER_SOFT = "SOFT"

    COVER_CHOICES = [
        (COVER_HARD, "Hard cover"),
        (COVER_SOFT, "Soft cover"),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES,
        default=COVER_SOFT
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"
