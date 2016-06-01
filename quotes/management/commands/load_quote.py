""" Loads initial quote & brief template, sets group permissions.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from gallant.models import Service
from guardian.shortcuts import assign_perm
from moneyed.classes import Money
from quotes.models import Quote, QuoteTemplate, Section


class Command(BaseCommand):
    help = 'Loads an initial quote template + sections and adds view permissions for "users" group.'

    def handle(self, **kwargs):
        load_quote()


def load_quote():
    UserModel = get_user_model()
    user = UserModel.objects.get(email='AnonymousUser')

    services = []

    quote = Quote.objects.create(name='Example - Branding', user=user)
    quote_template = QuoteTemplate.objects.create(quote=quote, user=user)

    s = Service.objects.create(
        name={'en': 'Identity'},
        index=0,
        cost=Money(2000.0, 'USD'),
        user=user, type=0, quantity=1,
        description={
            'en': u'A logo is a central part of the identity of a company, product, or service. Our identity development package includes:\n\n\u2013 Logo creation\n\u2013 Institutional logo palette\n\u2013 Textures or patterns upon request\n\u2013 Typeface selection (custom made typeface upon request)\n\n\u2013 Mood-boards:\nAt the beginning of the project, we\'ll develop \'mood-boards\' which will explore several different directions the project could take. These boards will help us involve you in the creative process, and ensures that the solution we choose to develop meets your expectations.'}
    )
    services.append(s)

    s = Service.objects.create(
        name={'en': 'Stationery Set'},
        index=1,
        cost=Money(500.0, 'USD'),
        user=user, type=0, quantity=1,
        description={
            'en': u'The following stationery elements are included in this project. Elements are interchangeable. We recommend the following:\n\n\u2013 Business card\n\u2013 Email signature\n\u2013 Letterhead\n\u2013 Envelope\n\u2013 Folder'}
    )
    services.append(s)

    s = Service.objects.create(
        name={'en': 'Product Packaging'},
        index=5,
        cost=Money(750.0, 'USD'),
        user=user, type=1, quantity=1,
        description={
            'en': u'We\'ll design brand adaptations to the following packaging elements:\n\n\u2013 Boutique bag (3 sizes)\n\u2013 Product packaging design (2 sizes)'}
    )
    services.append(s)

    quote.services.add(*services)

    set_quote_perms(quote_template)


def set_quote_perms(quote_template):
    users_group = Group.objects.get(name='users')

    quote = quote_template.quote

    assign_perm('view_quotetemplate', users_group, quote_template)
    assign_perm('view_quote', users_group, quote)
