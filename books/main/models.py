from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator


User = get_user_model()


class Book(models.Model):
    """ Модель книги """

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
        unique=True
    )
    published_at = models.PositiveIntegerField(
        verbose_name='Год издания',
        validators=[
            MaxValueValidator(
                datetime.now().year,
                'Год издания не может превышать текущий!')
        ]
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    authors = models.ManyToManyField(
        to=User,
        related_name='books',
        verbose_name='Автор(ы)'
    )
    is_achieved = models.BooleanField(
        default=False,
        verbose_name='Книга в архиве?'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Comment(models.Model):
    """ Модель комментария """

    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Книга'
    )
    published_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время создания/изменения'
    )

    def __str__(self):
        return f'{self.book}|{self.author}'

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

