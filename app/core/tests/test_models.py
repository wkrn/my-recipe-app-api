from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """emailによるユーザー作成ができるかのテスト"""
        email = 'wkrn@gmail.com'
        password = 'wkrn5313'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalizes(self):
        """新しいユーザのemailが標準化されてるかのテスト"""
        email = 'wkrn@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'wkrn5313')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """email無しのユーザー作成でerrorを起こすかのテスト"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'wkrn5313')

    def test_create_new_superuser(self):
        """新たなスーパーユーザの作成テスト"""
        user = get_user_model().objects.create_superuser(
            'wkrn@gmail.com',
            'wkrn5313'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
