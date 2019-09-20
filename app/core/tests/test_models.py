from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@gmail.com', password='wkrn5313'):
    """サンプルユーザの作成"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """タグのストリング表示をテストする"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ingredientのストリングが表示されるかのテスト"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """recipeストリングの表示テスト"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)
