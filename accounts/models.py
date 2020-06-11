from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from base_backend.models import cascade, do_nothing
from base_backend.validators import phone_validator
from generic_backend.models import BaseModel


class User(AbstractUser):
    TYPE = (('P', _('Patient')), ('PRO', _('Professional')))

    user_type = models.CharField(choices=TYPE, max_length=4, default='P')

    REQUIRED_FIELDS = ['email', 'password', 'user_type']

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


@receiver(post_save, sender=User)
def send_sms_signal(sender, instance, created, raw, **kwargs):
    if created and not raw:
        # from base_backend.utils import phone_sms_verification
        # phone_sms_verification(instance.phone)
        # if instance.user_type == 'C':
        #     Address.objects.create(address=instance.address, belongs_to=instance.client)
        instance.is_active = True
        instance.save()
