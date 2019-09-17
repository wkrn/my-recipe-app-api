from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """新しいユーザの作成と保存"""

        if not email:
            raise ValueError('ユーザはメールアドレスが必須です')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """新たなスーパーユーザの作成"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """usernameの代わりにemailを使ってユーザを作成するカスタムユーザー"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    # usernameの代わりにemailを使う。次にsettings.pyに行って、
    # AUTH_USER_MODEL = 'core.User'を追加
    USERNAME_FIELD = 'email'