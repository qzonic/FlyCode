from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from djoser.serializers import UserSerializer
from rest_framework import serializers

from main.models import Book, Comment


User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Author """

    books_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'books_count'
        )

    def get_books_count(self, obj):
        return obj.books.count()


class BookReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Book(чтение) """

    authors = AuthorSerializer(
        read_only=True,
        many=True
    )
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'name',
            'published_at',
            'authors',
            'description',
            'comments_count'
        )

    def get_comments_count(self, obj):
        return obj.comments.count()


class BookWriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Book(запись) """

    authors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
    )
    is_achieved = serializers.BooleanField(default=False)

    class Meta:
        model = Book
        fields = (
            'name',
            'published_at',
            'authors',
            'description',
            'is_achieved'
        )

    def validate_authors(self, obj):
        user = self.context.get('request').user
        if user not in obj:
            raise serializers.ValidationError(
                f'{obj}В авторах обязательно должен быть указан пользователь, создающий запись'
            )
        return obj

    def to_representation(self, instance):
        return BookReadSerializer(instance).data

    @atomic
    def set_authors(self, model, authors):
        model.authors.set(authors)

    @atomic
    def create(self, validated_data):
        authors = validated_data.pop('authors')
        books = super().create(validated_data)
        self.set_authors(books, authors)
        return books

    @atomic
    def update(self, instance, validated_data):
        if 'authors' in validated_data:
            authors = validated_data.pop('authors')
            instance.authors.clear()
            self.set_authors(instance, authors)
        return super().update(instance, validated_data)


class CommentReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Comment(чтение) """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'book',
            'published_at',
            'text'
        )


class CommentWriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Comment(запись) """

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = (
            'author',
            'text'
        )

    def to_representation(self, instance):
        return CommentReadSerializer(instance).data
