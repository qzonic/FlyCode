from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from main.models import Book, Comment


User = get_user_model()


class TestBook(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestBook, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='first_user'
        )
        cls.second_user = User.objects.create_user(
            username='second_user'
        )
        cls.first_author = Author.objects.create(
            first_name='Петр',
            last_name='Петров',
            slug='Petr-Petrov'
        )
        cls.second_author = Author.objects.create(
            first_name='Иван',
            last_name='Иванов',
            slug='Ivan-Ivanov'
        )
        cls.first_book = Book.objects.create(
            name='Книга 1',
            description='Тестовое описание книги 1',
            published_at=2023
        )
        cls.second_book = Book.objects.create(
            name='Книга 2',
            description='Тестовое описание книги 2',
            published_at=2022
        )

    def setUp(self) -> None:
        self.first_book.authors.add(self.first_author)
        self.second_book.authors.add(self.second_author)

        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.first_user)

    def test_pages_uses_correct_template(self):
        pages_names_templates = {
            reverse('main:books_list'): 'main/index.html',
            reverse(
                'main:books_detail',
                kwargs={'pk': self.first_book.id}
            ): 'main/book_detail.html',
            reverse(
                'main:author_books',
                kwargs={'slug': self.second_author.slug}
            ): 'main/index.html'
        }
        for reverse_name, template in pages_names_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template, reverse_name)

    def test_pages_show_correct_context(self):
        pages_names_templates = {
            reverse('main:books_list'): 'books',
            reverse(
                'main:books_detail',
                kwargs={'pk': self.first_book.id}
            ): 'book',
            reverse(
                'main:author_books',
                kwargs={'slug': self.first_author.slug}
            ): 'books'
        }
        for reverse_name, ctx in pages_names_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if ctx != 'book':
                    book = response.context.get(ctx)[0]
                else:
                    book = response.context.get(ctx)
                self.assertEqual(
                    book.name, 'Книга 1')
                self.assertIn(self.first_author, book.authors.all())

    def test_search_books_by_name(self):
        search_data = {
            'query': 'Книга 1'
        }
        response = self.guest_client.post(
            reverse('main:search_books'),
            data=search_data,
            follow=True
        )
        self.assertEqual(
            response.context.get('books')[0].name,
            search_data['query']
        )

    def test_create_comment_by_authorized_client(self):
        comment_data = {
            'text': 'test'
        }
        response = self.guest_client.post(reverse(
            'main:books_detail',
            kwargs={'pk': self.first_book.id}
        ),
            data=comment_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_comment_by_guest_client(self):
        comment_data = {
            'text': 'test'
        }
        response = self.guest_client.post(reverse(
            'main:books_detail',
            kwargs={'pk': self.first_book.id}
        ), comment_data)
        self.assertRedirects(response, reverse('users:login'))

