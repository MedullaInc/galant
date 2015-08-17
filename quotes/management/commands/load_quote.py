""" Loads initial quote & brief template, sets group permissions.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from gallant.models import Service
from guardian.shortcuts import assign_perm
from moneyed.classes import Money
from quotes.models import Quote, QuoteTemplate, TextSection, ServiceSection


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, **kwargs):
        load_quote()


def load_quote():
    UserModel = get_user_model()
    user = UserModel.objects.get(email='AnonymousUser')

    sections = []
    services = []

    quote = Quote.objects.create(name='Example - Branding', user=user)
    quote_template = QuoteTemplate.objects.create(quote=quote, user=user)

    sections.append(
        TextSection.objects.create(
            index=0, user=user, name='intro',
            title={'en': 'Hello!'},
            text={
                'en': 'We\'re an independent firm that specializes in brand development and positioning in all types of media. Our approach combines graphic design, brand consulting, and marketing strategy guided by tangible data.\n\nA carefully thought out, well positioned brand is a powerful asset to the value of a company. It\'s both a sales tool, and a differentiator when competing on the global stage.\n\nTo deliver a quality brand, exceptional creative talent is merely our starting point. Our in-depth consumer analysis, business sense, and marketing experience all help deliver a top-quality product that conveys your company\'s best qualities.'}
        )
    )

    sections.append(
        TextSection.objects.create(
            index=1, user=user, name='margin',
            title={'en': 'Notes'},
            text={
                'en': 'Once this proposal is authorized by you, the client, we will develop a timeline with delivery dates for each one of these tasks.\n\nCosts for photography, video, complex illustrations, and other such extras are not included.\n\nEditorial and copywriting costs are not included.\n\nCosts for printing, media contracts, and / or materials are not included.\n\nFor business card design, we include 10 design changes. Each extra change will have a cost of $20 USD.\n\nAny significant change requested after start of work / delivery will be subject to extra charges of up to 30% in addition to the total price quoted.\n\nThis quote is valid for 30 calendar days after its delivery.'},
        )
    )

    sections.append(
        TextSection.objects.create(
            index=5, user=user, name='section_4',
            title={'en': 'Payments'},
            text={
                'en': 'We require 50% of the quoted total up front.\n\nA 40% payment should be made before our first delivery.\n\nThe remaining 10% must be paid on final delivery.'}
        )
    )

    s = Service.objects.create(
        name={'en': 'Identity'},
        cost=Money(2000.0, 'USD'),
        user=user, type=0, quantity=1,
        description={
            'en': 'A logo is a central part of the identity of a company, product, or service. Our identity development package includes:\n\n\u2013Logo creation\n\u2013Institutional logo palette\n\u2013Textures or patterns upon request\n\u2013Typeface selection (custom made typeface upon request)\n\n\u2013Mood-boards:\nAt the beginning of the project, we\'ll develop \'mood-boards\' which will explore several different directions the project could take. These boards will help us involve you in the creative process, and ensures that the solution we choose to develop meets your expectations.'}
    )
    services.append(
        ServiceSection.objects.create(index=2, user=user,
                                      name='section_1', service=s)
    )

    s = Service.objects.create(
        name={'en': 'Stationery Set'},
        cost=Money(500.0, 'USD'),
        user=user, type=0, quantity=1,
        description={
            'en': 'The following stationery elements are included in this project. Elements are interchangeable. We recommend the following:\n\n\u2013 Business card\n\u2013 Email signature\n\u2013 Letterhead\n\u2013 Envelope\n\u2013 Folder'}
    )
    services.append(
        ServiceSection.objects.create(index=3, user=user,
                                      name='section_2', service=s)
    )

    s = Service.objects.create(
        name={'en': 'Product Packaging'},
        cost=Money(750.0, 'USD'),
        user=user, type=1, quantity=1,
        description={
            'en': 'We\'ll design brand adaptations to the following packaging elements:\n\n\u2013 Boutique bag (3 sizes)\n\u2013 Product packaging design (2 sizes)'}
    )
    services.append(
        ServiceSection.objects.create(index=4, user=user,
                                      name='section_3', service=s)
    )

    quote.sections.add(*sections)
    quote.services.add(*services)

    set_quote_perms(quote_template)


def set_quote_perms(quote_template):
    users_group = Group.objects.get(name='users')

    quote = quote_template.quote

    assign_perm('view_quotetemplate', users_group, quote_template)
    assign_perm('view_quote', users_group, quote)

    for s in quote.all_sections():
        assign_perm('view_section', users_group, s)
