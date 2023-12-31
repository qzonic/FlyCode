# Generated by Django 4.2.2 on 2023-07-03 18:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "published_at",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(
                                2023, "Год издания не может превышать текущий!"
                            )
                        ],
                        verbose_name="Год издания",
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "is_achieved",
                    models.BooleanField(default=False, verbose_name="Книга в архиве?"),
                ),
                (
                    "authors",
                    models.ManyToManyField(
                        related_name="books",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор(ы)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Книга",
                "verbose_name_plural": "Книги",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст комментария")),
                (
                    "published_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата и время создания/изменения"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="main.book",
                        verbose_name="Книга",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
                "ordering": ["-published_at"],
            },
        ),
    ]
