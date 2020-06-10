"""
creates permission groups
to be used right after migrations
"""
from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create groups and initialize default permissions'

    GROUPS = ['patient', 'doctor', 'caregiver', 'staff', 'administration_1', 'administration_2', 'admin']

    # RECIPE_APP_MODELS = list(apps.get_app_config("recipe").models)
    # RESTAURANTS_APP_MODELS = list(apps.get_app_config("restaurants").models)
    # MANAGEMENT_APP_MODELS = list(apps.get_app_config("management").models)
    # DELIVERY_APP_MODELS = list(apps.get_app_config("delivery").models)

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', type=bool,
                            help='forces the re-attribution of perms to the groups, should be used'
                                 ' in case of adding new models')

    def handle(self, *args, **options):
        force = options.get('force', False)
        self._init_patient(force=force)
        self._init_doctor(force=force)
        self._init_administration_2(force=force)
        self._init_caregiver(force=force)
        self._init_admin(force=force)
        self._init_staff()
        self._init_administration_1()
        self._init_administration_2()
        print('created default groups and permissions.')

    def _init_patient(self, force=False):
        delivery_perms = []
        self._init_group_('patient', delivery_perms, force=force)

    def _init_doctor(self, force=False):
        all_models = []
        self._init_group_('doctor', all_models, force=force)

    def _init_caregiver(self, force=False):
        all_models = []
        self._init_group_('caregiver', all_models, force=force)

    def _init_staff(self, force=False):
        all_models = []
        self._init_group_('staff', all_models, force=force)

    def _init_administration_1(self, force=False):
        owner_perms = []
        self._init_group_('administration_1', owner_perms, force=force)

    def _init_administration_2(self, force=False):
        owner_perms = []
        self._init_group_('administration_2', owner_perms, force=force)

    def _init_admin(self, force=False):
        all_models = []
        self._init_group_('admin', all_models, force=force)

    def _init_group_(self, group_name: str, perms: list, perm_type=None, force=False) -> None:
        new_group, created = Group.objects.get_or_create(name=group_name)
        # if not created and not force:
        #     print('group {} already created, if you want to force '
        #           'the re-attribution of permissions please add  "--force=True" to the command .'.format(group_name))
        #     return
        # for perm in perms:
        #     try:
        #         content_type = ContentType.objects.get(model=perm)
        #         if perm_type is not None:
        #             permissions = Permission.objects.filter(content_type=content_type, codename__startswith=perm_type)
        #         else:
        #             permissions = Permission.objects.filter(content_type=content_type)
        #         new_group.permissions.add(*permissions)
        #         print('{} group: adding all permissions on {}'.format(group_name, perm))
        #     except ContentType.DoesNotExist:
        #         pass
