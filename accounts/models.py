from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from base_backend.models import cascade, do_nothing
from base_backend.validators import phone_validator
from generic_backend.models import BaseModel


class User(AbstractUser):
    REQUIRED_FIELDS = ["first_name", "last_name", 'email', 'password']

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )


class Profile(BaseModel):
    GENDERS = (('M', _('Male')), ('F', _('Female')))

    photo = models.ImageField(upload_to="media/pictures")
    address = models.CharField(max_length=255)
    city = models.ForeignKey('localization_management.City', on_delete=do_nothing, related_name="citizens")
    gender = models.CharField(choices=GENDERS, max_length=1)
    phone = models.CharField(_("Phone Number"), validators=[phone_validator], max_length=50, unique=True)
    user = models.OneToOneField('accounts.User', on_delete=cascade, related_name="profile")
    birth_date = models.DateField()


class AccessTimes(BaseModel):
    start_hour = models.TimeField()
    finish_hour = models.TimeField()
