from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book-detail'
    )

    class Meta:
        model = Author
        fields = [
            'url',
            'id',
            'name',
            'biography',
            'birth_year',
            'death_year',
            'books'
        ]

class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='author-detail'
    )
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True,
        help_text="ID автора"
    )

    class Meta:
        model = Book
        fields = [
            'url',
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
        return Book.objects.create(author=author, **validated_data)