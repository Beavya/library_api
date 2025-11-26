from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

BOOK_GENRES = [
    ('fiction', 'Художественная литература'),
    ('fantasy', 'Фантастика'),
    ('sci_fi', 'Научная фантастика'),
    ('detective', 'Детектив'),
    ('romance', 'Романтика'),
    ('horror', 'Ужасы'),
    ('history', 'История'),
    ('biography', 'Биография'),
    ('education', 'Учебная литература'),
    ('poetry', 'Поэзия'),
    ('drama', 'Драма'),
    ('other', 'Другое'),
]

class Author(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Имя автора")
    )
    biography = models.TextField(
        blank=True,
        verbose_name=_("Биография")
    )
    birth_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Год рождения")
    )
    death_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Год смерти")
    )

    class Meta:
        verbose_name = _("Автор")
        verbose_name_plural = _("Авторы")
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name=_("Название книги")
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name=_("Автор")
    )
    year = models.PositiveIntegerField(
        verbose_name=_("Год выпуска"),
        validators=[
            MinValueValidator(1000, message=_("Год должен быть не меньше 1000")),
            MaxValueValidator(9999, message=_("Год должен быть не больше 9999"))
        ]
    )
    genre = models.CharField(
        max_length=20,
        choices=BOOK_GENRES,  # ← Жанры прямо из модели!
        verbose_name=_("Жанр книги")
    )
    category = models.CharField(
        max_length=100,
        verbose_name=_("Категория книги")
    )
    publisher = models.CharField(
        max_length=100,
        verbose_name=_("Издательство")
    )
    cover = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        verbose_name=_("Обложка")
    )
    file = models.FileField(
        upload_to='books/',
        verbose_name=_("Файл книги")
    )

    class Meta:
        verbose_name = _("Книга")
        verbose_name_plural = _("Книги")
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'year', 'publisher'],
                name='unique_book_edition'
            )
        ]
        ordering = ['title', 'year']

    def __str__(self):
        return f"{self.title} ({self.year}) — {self.author.name}"