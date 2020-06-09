from django.db import models

# Create your models here.
from generic_backend.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
