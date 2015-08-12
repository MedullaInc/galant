import inspect
from custom_user.models import AbstractEmailUser
from django.db import models as m
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.forms.widgets import CURRENCY_CHOICES
from gallant import fields as gf
from guardian.utils import get_user_obj_perms_model
from django_countries.fields import CountryField
from polymorphic import PolymorphicModel
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms_for_model
from polymorphic.manager import PolymorphicManager
from django.contrib.contenttypes.models import ContentType


class ContactInfo(m.Model):
    phone_number = m.CharField(validators=[gf.PHONE_REGEX], max_length=15)
    address = m.CharField(max_length=255)
    address_2 = m.CharField(max_length=255, blank=True)
    city = m.CharField(max_length=127)
    state = m.CharField(max_length=127)
    zip = m.CharField(validators=[gf.ZIP_REGEX], max_length=12)
    country = CountryField(default='US')


class GallantUser(AbstractEmailUser):
    """
    Custom Gallant user
    """
    name = m.CharField(max_length=255)
    company_name = m.CharField(max_length=255, blank=True)
    contact_info = m.ForeignKey(ContactInfo, null=True)

    @property
    def username(self):
        return self.email

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class UserModel(m.Model):
    user = m.ForeignKey(GallantUser)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(UserModel, self).save(*args, **kwargs)
        for perm in get_perms_for_model(self):
            assign_perm(perm.codename, self.user, self)


class PolyUserModel(PolymorphicModel):
    user = m.ForeignKey(GallantUser)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(PolyUserModel, self).save(*args, **kwargs)
        for perm in get_perms_for_model(self):
            assign_perm(perm.codename, self.user, self)


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

    def all_for(self, user, perm):
        return get_objects_for_user(user, perm, self, accept_global_perms=False)

    def get_for(self, user, perm, *args, **kwargs):
        obj = super(UserManagerMethodsMixin, self).get(*args, **kwargs)
        if user.has_perm(perm, obj):
            return obj
        else:
            return None

    def _caller_blocked(self):  # Allow certain modules to call blocked methods
        mod = inspect.getmodule(inspect.stack()[2][0])  # Who is calling us?
        return all(app not in mod.__name__ for app in ['autofixture', 'django'])


class UserModelManager(UserManagerMethodsMixin, m.Manager):
    use_for_related_fields = True


class PolyUserModelManager(UserManagerMethodsMixin, PolymorphicManager):
    use_for_related_fields = True

    # WARNING: this may be inefficient in the long run. May switch to non-polymorphic.
    def all_for(self, user, perm):
        ids_queryset = self._get_valid_ids(self.model, user, perm)

        for rel in self.model._meta.related_objects:
            if issubclass(rel.related_model, self.model):
                ids_queryset = ids_queryset | self._get_valid_ids(rel.related_model, user, perm)

        return self.filter(pk__in=ids_queryset)

    @staticmethod
    def _get_valid_ids(model, user, perm):
        user_model = get_user_obj_perms_model(model)
        ctype = ContentType.objects.get_for_model(model)
        return user_model.objects\
                           .filter(user=user)\
                           .filter(permission__content_type=ctype)\
                           .filter(permission__codename=perm)\
            .values_list('object_pk', flat=True)


class Note(UserModel):
    text = m.TextField(help_text='User comment / note.')
    created = m.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_note', 'View note'),
        )

    objects = UserModelManager()


class ServiceType(gf.ChoiceEnum):
    Branding = 0
    Design = 1
    Architecture = 2
    Advertising = 3
    Production = 4
    Illustration = 5
    Industrial_Design = 6
    Fashion_Design = 7
    Interior_Design = 8


class Service(UserModel):
    """
    A service to be rendered for a client, will appear on Quotes. When associated with a project / user, it should
    be displayed as a 'deliverable' instead.
    """
    # name = m.ForeignKey(ULText, related_name='name')
    name = gf.ULCharField()
    description = gf.ULTextField(null=True)
    # TODO: brief = ServiceBrief()

    # currency is chosen based on client preference
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    quantity = m.IntegerField()
    type = m.CharField(max_length=2, choices=ServiceType.choices())

    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_services')

    notes = m.ManyToManyField(Note)

    def get_total_cost(self):
        total = self.cost * self.quantity
        for sub in self.sub_services.all_for(self.user, 'view_service'):
            total += sub.get_total_cost()

        return total

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_service', 'View service'),
        )

    objects = UserModelManager()


class ClientType(gf.ChoiceEnum):
    Individual = 0
    Organization = 1


class ClientSize(gf.ChoiceEnum):
    Micro = 0
    Small = 1
    Medium = 2
    Large = 3


class ClientStatus(gf.ChoiceEnum):
    Approached = 0
    Quoted = 1
    Brief_Sent = 2
    Pending_Payment = 3
    Pending_Deliverables = 4
    Settled = 5
    Past_Due = 6
    Check_Notes = 7
    Blacklisted = 8


class Client(UserModel):
    name = m.CharField(max_length=255)
    email = m.EmailField(blank=True)
    phone_number = m.CharField(validators=[gf.PHONE_REGEX], blank=True, max_length=15)
    address = m.TextField(blank=True)

    type = m.CharField(max_length=2, choices=ClientType.choices())
    size = m.CharField(max_length=2, choices=ClientSize.choices())
    status = m.CharField(max_length=2, choices=ClientStatus.choices())

    language = m.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    notes = m.ManyToManyField(Note)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_client', 'View client'),
        )

    objects = UserModelManager()


class ProjectStatus(gf.ChoiceEnum):
    On_Hold = 0
    Pending_Assignment = 1
    Active = 2
    Overdue = 3
    Completed = 4


class Project(UserModel):
    name = m.CharField(max_length=255)
    status = m.CharField(max_length=2, choices=ProjectStatus.choices(), default=ProjectStatus.Pending_Assignment.value)

    notes = m.ManyToManyField(Note)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_project', 'View project'),
        )

    objects = UserModelManager()
