from django.contrib import admin

# Register your models here.
from base_backend.admin import register_app_models

register_app_models('accounts')
register_app_models('auth')
