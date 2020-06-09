from django.contrib.auth.models import User as BaseDjangoUser, PermissionsMixin

from generic_backend.models import BaseModel


class User(BaseDjangoUser, PermissionsMixin, BaseModel):
    # TODO: figure this out
    pass


class Profile(BaseModel):
    pass


class AccessTimes(BaseModel):
    pass


