from django.contrib.auth import get_user_model
from rest_framework import permissions, status
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
                type=user.user_type,
                first_name=user.first_name,
                last_name=user.last_name
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
                Returns the object the view is displaying.

                You may want to override this if you need to provide non-standard
                queryset lookups.  Eg if objects are referenced using multiple
                keyword arguments in the url conf.
                """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
            # May raise a permission denied
            self.check_object_permissions(self.request, obj)
        except Profile.DoesNotExist:
            obj = None

        return obj


class AccessTimesViewSet(ModelViewSet):
    serializer_class = AccessTimesSerializer
    queryset = AccessTimes.objects.all()
    permission_classes = [mperms.IsAdminOrReadOnly]
