from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.db import transaction


class Command(BaseCommand):
    help = 'Add a user and generate a registration link (change base URL for non-production).'

    def add_arguments(self, parser):
        parser.add_argument('user_email',
                            help='Email of user to create.')

    def handle(self, **options):
        manage_agency(options)

@transaction.atomic
def manage_agency(options):
    email = options['user_email']
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        user = UserModel.objects.create_user(email=email)
    token = default_token_generator.make_token(user)
    print 'http://galant.com/en/register/' + str(user.id) + '?token=%s' % token
