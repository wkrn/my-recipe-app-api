from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """システムに新たなユーザを作る"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """新たなユーザ認証トークンを作る"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
