from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import Profile, AccessTimes
from accounts.serializers import UserSerializer, ProfileSerializer, AccessTimesSerializer
from base_backend import permissions as mperms


class LoginApi(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context=dict(request=request))
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            dict(
                token=token.key,
                user_id=user.pk,
                email=user.email,
                username=user.username,
                type=user.user_type
            )
        )


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AccessTimesViewSet(ModelViewSet):
    serializer_class = AccessTimesSerializer
    queryset = AccessTimes.objects.all()
    permission_classes = [mperms.IsAdminOrReadOnly]
