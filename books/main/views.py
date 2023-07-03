from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import CommentForm, SearchForm
from .models import Book
from .mixins import ArchivedBookMixin


User = get_user_model()


class AuthorBookListView(ListView):
    model = User
    template_name = 'main/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        username = self.kwargs.get('username')
        return super().get_queryset().filter(username=username).first().books.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        context['title'] = f'Книги {author.username}'
        return context


class BookListView(ArchivedBookMixin, ListView):
    model = Book
    template_name = 'main/index.html'
    context_object_name = 'books'
    search_form = SearchForm


class BookDetailView(ArchivedBookMixin, DetailView):
    model = Book
    context_object_name = 'book'
    search_form = SearchForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and self.request.method == 'POST':
            return HttpResponseRedirect(reverse('users:login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST or None)
        if form.is_valid():
            book = get_object_or_404(Book, pk=kwargs.get('pk'))
            new_comment = form.save(commit=False)
            new_comment.author = self.request.user
            new_comment.book = book
            new_comment.save()
            return HttpResponseRedirect(reverse(
                'main:books_detail',
                kwargs={'pk': kwargs.get('pk')}
            ))


class SearchView(ArchivedBookMixin, View):
    model = Book

    def post(self, request, *args, **kwargs):
        form = SearchForm(data=request.POST or None)
        if form.is_valid():
            books = self.get_queryset().filter(
                name__icontains=form.cleaned_data.get('query')
            )
            return render(
                request,
                'main/index.html',
                {
                    'books': books,
                    'title': 'Поиск',
                    'search_form': form
                }
            )
