from django.urls import path

from .views import AuthorBookListView, BookListView, BookDetailView, SearchView


app_name = 'main'


urlpatterns = [
    path('', BookListView.as_view(), name='books_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='books_detail'),
    path('author/<str:username>/', AuthorBookListView.as_view(), name='author_books'),
    path('search/', SearchView.as_view(), name='search_books')
]
