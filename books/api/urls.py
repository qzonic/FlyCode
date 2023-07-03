from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet, CommentViewSet


router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet, basename='books')
router.register(r'books/(?P<book_id>\d+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
