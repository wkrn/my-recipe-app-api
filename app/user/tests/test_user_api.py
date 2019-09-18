from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):
    """パブリックユーザーAPIのテスト"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """有効なペイロードを持ったユーザー作成が成功したかのテスト"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'wkrn5313',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """既に存在するユーザの作成が失敗するかのテスト"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'wkrn5313'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """パスワードが5文字以上でなければならないかのテスト"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """トークンがユーザに作られたかどうかのテスト"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'wkrn5313'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """有効でないクレデンシャルが与えられた時、トークンが作成されないことのテスト"""
        create_user(email='test@gmail.com', password='wkrn5313')
        payload = {'email': 'wkrn@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ユーザーが存在しない場合トークンが発行されないことのテスト"""
        payload = {
            'email': 'wkrn@gmail.com', 'password': 'wkrn5313'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """メールアドレスとパスワードが必要かのテスト"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
