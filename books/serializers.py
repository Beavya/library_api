from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'biography',
            'birth_year',
            'death_year',
            'books'
        ]

class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True,
        help_text="ID автора из списка существующих"
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'author_id',
            'year',
            'genre',
            'category',
            'publisher',
            'cover',
            'file'
        ]

    def create(self, validated_data):
        author = validated_data.pop('author_id')
        book = Book.objects.create(author=author, **validated_data)
        return book