from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Admin users can create/update/delete books.
        All users (including unauthenticated) can list/retrieve books.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
