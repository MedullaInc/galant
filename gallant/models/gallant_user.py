import inspect
from itertools import chain
from custom_user.models import AbstractEmailUser, EmailUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models as m
from djmoney.settings import CURRENCY_CHOICES
from guardian.utils import get_user_obj_perms_model, get_group_obj_perms_model
from polymorphic import PolymorphicModel
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms_for_model
from polymorphic.manager import PolymorphicManager
from django.contrib.contenttypes.models import ContentType
from polymorphic.query import PolymorphicQuerySet
from gallant import fields as gf
from django_countries.fields import CountryField


class ContactInfo(m.Model):
    phone_number = m.CharField(validators=[gf.PHONE_REGEX], max_length=20, blank=True)
    address = m.CharField(max_length=255, blank=True)
    address_2 = m.CharField(max_length=255, blank=True)
    city = m.CharField(max_length=127, blank=True)
    state = m.CharField(max_length=127, blank=True)
    zip = m.CharField(validators=[gf.ZIP_REGEX], max_length=12, blank=True)
    country = CountryField(default='US')


class GalantUserManager(EmailUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = super(GalantUserManager, self).create_user(email, password, **extra_fields)

        g = Group.objects.get(name='users')
        g.user_set.add(user)

        return user


class GallantUser(AbstractEmailUser):
    """
    Custom Gallant user
    """
    name = m.CharField(max_length=255)
    company_name = m.CharField(max_length=255, blank=True)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD',)
    contact_info = m.ForeignKey(ContactInfo, null=True)

    """
    To allow multiple users from a same agency access to the same objects, use the management
    command manage_agency to create an agency group and add users to it.
    """
    agency_group = m.ForeignKey(Group, null=True)

    objects = GalantUserManager()

    @property
    def username(self):
        return self.email

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class UserModel(m.Model):
    user = m.ForeignKey(GallantUser)

    deleted = m.BooleanField(default=False)
    deleted_by_parent = m.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(UserModel, self).save(*args, **kwargs)
        for perm in get_perms_for_model(self):
            assign_perm(perm.codename, self.user, self)
            if self.user.agency_group:
                assign_perm(perm.codename, self.user.agency_group, self)

    def soft_delete(self, deleted_by_parent=False):
        if deleted_by_parent is True:
            self.deleted_by_parent = deleted_by_parent

        self.deleted = True
        self.save()


class PolyUserModel(PolymorphicModel):
    user = m.ForeignKey(GallantUser)

    deleted = m.BooleanField(default=False)
    deleted_by_parent = m.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(PolyUserModel, self).save(*args, **kwargs)
        for perm in get_perms_for_model(self):
            assign_perm(perm.codename, self.user, self)
            if self.user.agency_group:
                assign_perm(perm.codename, self.user.agency_group, self)

    def soft_delete(self, deleted_by_parent=False):
        if deleted_by_parent is True:
            self.deleted_by_parent = deleted_by_parent

        self.deleted = True
        self.save()


class UserManagerMethodsMixin(object):
    ''' Block some common access methods to prevent programmer error, and provide safe methods
     to access by checking permissions. WARNING: Templates can still mistakenly call all(),
     since the logic to determine if it should be allowed is too dumb to recognize one of our
     own templates. Make sure to use objects_for template tag instead!
    '''

    def all(self):
        if self._caller_blocked():
            raise RuntimeError('Attempted to use all() via UserModelManager. Use all_for() instead.')
        return super(UserManagerMethodsMixin, self).all()

    def get(self, *args, **kwargs):
        if self._caller_blocked():
            raise RuntimeError('Attempted to use get() via UserModelManager. Use get_for() instead.')
        return super(UserManagerMethodsMixin, self).get(*args, **kwargs)

    def all_for(self, user, perm='view', show_deleted=False):
        perm = '%s_%s' % (perm, self.model._meta.model_name)
        if show_deleted:
            return get_objects_for_user(user, perm, self, accept_global_perms=False)
        else:
            return get_objects_for_user(user, perm, self, accept_global_perms=False).filter(deleted=False)

    def get_for(self, user, perm='view', *args, **kwargs):
        perm = '%s_%s' % (perm, self.model._meta.model_name)
        obj = super(UserManagerMethodsMixin, self).get(*args, **kwargs)
        if user.has_perm(perm, obj) and obj.deleted is False:
            return obj
        else:
            return None

    def _caller_blocked(self):  # Allow certain modules to call blocked methods
        mod = inspect.getmodule(inspect.stack()[2][0])  # Who is calling us?
        if not mod:
            return False
        return all(app not in mod.__name__ for app in ['autofixture', 'django', 'rest_framework'])


class UserModelManager(UserManagerMethodsMixin, m.Manager):
    use_for_related_fields = True


class PolyUserModelManager(UserManagerMethodsMixin, PolymorphicManager):
    use_for_related_fields = True
    queryset_class = PolymorphicQuerySet

    # WARNING: this may be inefficient in the long run. May switch to non-polymorphic.
    def all_for(self, user, perm='view'):
        perm = '%s_%s' % (perm, self.model._meta.model_name)
        ids_queryset = self._get_valid_ids(self.model, user, perm)

        for rel in self.model._meta.related_objects:
            if issubclass(rel.related_model, self.model):
                ids_queryset = chain(ids_queryset, self._get_valid_ids(rel.related_model, user, perm))

        return self.filter(pk__in=ids_queryset)

    @staticmethod
    def _get_valid_ids(model, user, perm):
        user_model = get_user_obj_perms_model(model)
        group_model = get_group_obj_perms_model(model)
        ctype = ContentType.objects.get_for_model(model)
        user_obj_query = user_model.objects\
                                   .filter(user=user)\
                                   .filter(permission__content_type=ctype)\
                                   .filter(permission__codename=perm)\
            .values_list('object_pk', flat=True)

        user_group_filter = {
            'group__%s' % get_user_model().groups.field.related_query_name(): user
        }
        group_obj_query = group_model.objects\
                                     .filter(**user_group_filter)\
                                     .filter(permission__content_type=ctype)\
                                     .filter(permission__codename=perm)\
            .values_list('object_pk', flat=True)

        return chain(user_obj_query, group_obj_query)

