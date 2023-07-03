
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    filters,
    decorators,
    permissions,
    mixins
)

from .filters import BookFilterSet
from .serializers import (
    AuthorSerializer,
    BookReadSerializer,
    BookWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer
)
from .permissions import (
    IsBookAuthorOrReadOnly,
    IsCommentAuthorOrReadOnly,
    IsCurrentUserOrReadOnly
)
from main.models import Book, Comment


User = get_user_model()


class UpdateRetrieveListMixin(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    pass


class AuthorViewSet(UpdateRetrieveListMixin):
    """ ViewSet для взаимодействия с сериализатором Author """

    queryset = User.objects.all()
    permission_classes = [IsCurrentUserOrReadOnly]
    serializer_class = AuthorSerializer

    @decorators.action(
        detail=False,
        methods=['get'],
        url_path='my',
        permission_classes=[permissions.IsAuthenticated]
    )
    def my(self, request):
        queryset = request.user.books.all()
        books = self.paginate_queryset(queryset)
        serializer = BookReadSerializer(
            books,
            many=True
        )
        return self.get_paginated_response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """ ViewSet для взаимодействия с сериализатором Book """

    permission_classes = [IsBookAuthorOrReadOnly]
    filterset_class = BookFilterSet
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_queryset(self):
        return Book.objects.filter(is_achieved=False)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookReadSerializer
        return BookWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ ViewSet для взаимодействия с сериализатором Comment """

    queryset = Comment.objects.all()
    permission_classes = [IsCommentAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentReadSerializer
        return CommentWriteSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        return Comment.objects.filter(book=book)

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs.get('book_id'))
        serializer.save(book=book)
