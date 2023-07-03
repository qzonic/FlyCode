from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


User = get_user_model()


class TestUser(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='first_user'
        )

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_signup_with_existing_username(self):
        signup_data = {
            'username': 'first_user',
            'password1': 'test_password132',
            'password2': 'test_password132'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=signup_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'A user with that username already exists.',
            response.context.get('form').errors['username'][0]
        )

    def test_signup_with_unexisting_username(self):
        signup_data = {
            'username': 'test_user',
            'password1': 'test_password132',
            'password2': 'test_password132'
        }
        user = User.objects.filter(
            username=signup_data['username']
        ).exists()
        self.guest_client.post(
            reverse('users:signup'),
            data=signup_data,
            follow=True
        )
        self.assertEqual(not user, User.objects.filter(
            username=signup_data['username']
        ).exists())
