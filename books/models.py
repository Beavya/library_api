from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя автора",
        help_text="Полное имя автора (например: Лев Толстой)"
    )
    biography = models.TextField(
        blank=True,
        verbose_name="Биография",
        help_text="Краткая биография или описание автора"
    )
    birth_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Год рождения"
    )
    death_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Год смерти"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название книги"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Автор"
    )
    year = models.PositiveIntegerField(
        verbose_name="Год выпуска"
    )
    genre = models.CharField(
        max_length=100,
        verbose_name="Жанр"
    )
    category = models.CharField(
        max_length=100,
        verbose_name="Категория"
    )
    publisher = models.CharField(
        max_length=100,
        verbose_name="Издательство"
    )
    cover = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        verbose_name="Обложка книги"
    )
    file = models.FileField(
        upload_to='books/',
        verbose_name="Файл книги (PDF, EPUB и т.д.)"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'year', 'publisher'],
                name='unique_book_edition'
            )
        ]
        ordering = ['title', 'year']

    def __str__(self):
        return f"{self.title} ({self.year}) — {self.author.name}"