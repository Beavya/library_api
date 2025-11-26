from rest_framework import viewsets, permissions, filters
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsAdminOrReadOnly

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'biography']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genre', 'category', 'publisher', 'author__name']

    def perform_create(self, serializer):
        serializer.save()