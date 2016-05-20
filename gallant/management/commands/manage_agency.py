from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Loads an initial brief template + questions and adds view permissions for "users" group.'

    def add_arguments(self, parser):
        parser.add_argument('-a', nargs=1, dest='user_add', metavar='EMAIL',
                            help='Add user with given email to agency group.')
        parser.add_argument('-r', nargs=1, dest='user_del', metavar='EMAIL',
                            help='Remove user with given email from agency group.')
        parser.add_argument('-d', action='store_true',
                            help='Remove agency group and all user associations.')
        parser.add_argument('agency_group',
                            help='Group name (string) of agency to use. Will be created if '
                                 'it doesn\'t exist.')

    def handle(self, **options):
        manage_agency(options)

@transaction.atomic
def manage_agency(options):
    group, created = Group.objects.get_or_create(name=options['agency_group'])
    if options['user_add']:
        user = get_user_model().objects.get(email=options['user_add'].pop())
        if user.agency_group:
            user.agency_group.user_set.remove(user)
        group.user_set.add(user)
        user.agency_group = group
        user.save()
    elif options['user_del']:
        user = get_user_model().objects.get(email=options['user_del'].pop())
        group.user_set.remove(user)
        user.agency_group = None
        user.save()
    elif options['d']:
        for user in group.user_set.all():
            user.agency_group = None
            user.save()
        group.delete()


