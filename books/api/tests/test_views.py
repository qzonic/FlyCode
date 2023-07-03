from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Book, Comment


User = get_user_model()


class TestAuthor(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAuthor, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='admin',
            is_staff=True
        )
        cls.second_user = User.objects.create_user(
            username='second_user'
        )

    def setUp(self) -> None:
        self.admin_user = APIClient()
        token = RefreshToken.for_user(self.first_user)
        self.admin_user.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        self.guest_user = APIClient()

    def test_get_authors_list(self):
        authors_in_db = 2

        response = self.guest_user.get('/api/authors/')
        self.assertEqual(response.json()['count'], authors_in_db)

    def test_patch_user_by_another_user(self):
        author = User.objects.filter(
            username='admin'
        ).first()
        author_data = {
            'first_name': 'Алекей'
        }
        response = self.guest_user.patch(f'/api/authors/{author.id}/', author_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_by_self(self):
        author = User.objects.filter(
            username='admin'
        ).first()
        author_data = {
            'first_name': 'Алекей'
        }
        response = self.admin_user.patch(f'/api/authors/{author.id}/', author_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_name = response.json()['first_name']
        self.assertEqual(first_name, author_data['first_name'])

    def test_my_endpoint(self):
        response = self.guest_user.get('/api/authors/my/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.admin_user.get('/api/authors/my/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBook(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(TestBook, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='admin',
            is_staff=True
        )
        cls.second_user = User.objects.create_user(
            username='second_user'
        )
        cls.first_book = Book.objects.create(
            name='Книга 1',
            description='Тестовое описание книги 1',
            published_at=datetime.now().year
        )

    def setUp(self) -> None:
        self.authorized_user = APIClient()
        token = RefreshToken.for_user(self.first_user)
        self.authorized_user.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        self.guest_user = APIClient()

        self.first_book.authors.add(self.first_user)

    def test_create_book_by_guest_user(self):
        book_data = {
            'name': 'Книга 2',
            'description': 'Тестовое описание книги 2',
            'authors': [1],
            'published_at': 2023
        }
        response = self.guest_user.post('/api/books/', book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_by_authorized(self):
        book_data = {
            'name': 'Книга 2',
            'description': 'Тестовое описание книги 2',
            'authors': [
                self.first_user.id
            ],
            'published_at': 2023
        }
        response = self.authorized_user.post('/api/books/', book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_with_more_authors(self):
        book_data = {
            'name': 'Книга 2',
            'description': 'Тестовое описание книги 2',
            'authors': [
                self.first_user.id,
                self.second_user.id
            ],
            'published_at': 2023
        }
        response = self.authorized_user.post('/api/books/', book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_book_by_guest_user(self):
        response = self.guest_user.delete(f'/api/books/{self.first_book.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_book_by_guest_user(self):
        book_data = {
            'name': 'Новое название'
        }
        response = self.guest_user.patch(f'/api/books/{self.first_book.id}/', book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_book_by_author(self):
        book_data = {
            'name': 'Новое название'
        }

        response = self.authorized_user.patch(f'/api/books/{self.first_book.id}/', book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_books(self):
        response = self.guest_user.get(f'/api/books/?authors={self.first_user.username}')
        self.assertEqual(
            response.json()['results'][0]['name'],
            self.first_book.name
        )

    def test_search_first_book(self):
        response = self.guest_user.get(f'/api/books/?search=Книга 1')
        self.assertEqual(
            response.json()['results'][0]['name'],
            self.first_book.name
        )


class TestComment(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(TestComment, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='admin',
            is_staff=True
        )
        cls.second_user = User.objects.create_user(
            username='second_user'
        )
        cls.third_user = User.objects.create_user(
            username='third_user'
        )
        cls.first_book = Book.objects.create(
            name='Книга 1',
            description='Тестовое описание книги 1',
            published_at=datetime.now().year
        )

    def setUp(self) -> None:
        self.admin_user = APIClient()
        token = RefreshToken.for_user(self.first_user)
        self.admin_user.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        self.second_client = APIClient()
        token = RefreshToken.for_user(self.second_user)
        self.second_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        self.third_client = APIClient()
        token = RefreshToken.for_user(self.third_user)
        self.third_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        self.anonymous = APIClient()

        self.first_book.authors.add(self.first_user)

    def test_create_comment_by_unauthorized(self):
        comment_data = {
            'text': 'Тестовый коммент',
        }
        response = self.anonymous.post(f'/api/books/{self.first_book.id}/comments/', comment_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_by_authorized_user(self):
        comment_data = {
            'text': 'Тестовый коммент',
            'book': self.first_book.id
        }
        first_response = self.second_client.post(f'/api/books/{self.first_book.id}/comments/', comment_data)
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        response = self.third_client.delete(
            f'/api/books/{self.first_book.id}/comments/{first_response.json()["id"]}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
