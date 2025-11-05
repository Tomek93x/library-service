from django.contrib import admin

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""

    list_display = ["title", "author", "cover", "inventory", "daily_fee"]
    list_filter = ["cover"]
    search_fields = ["title", "author"]
