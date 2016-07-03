from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from gallant import models as g
import django_countries
import csv

class Command(BaseCommand):
    help = 'Loads a CSV from Capsule CRM export.'

    def add_arguments(self, parser):
        parser.add_argument('user_email',
                            help='User for which to add data.')
        parser.add_argument('file_name',
                            help='CSV file to parse.')

    def handle(self, **options):
        load_capsule_csv(options)

@transaction.atomic
def load_capsule_csv(options):
    user = get_user_model().objects.get(email=options['user_email'])

    with open(options['file_name'], 'rb') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        for row in reader:
            if row['Type'] == 'Organization':
                continue

            country = 'US'

            if row['Country'] != 'United States':
                for code, name in django_countries.Countries():
                    if len(row['Country']) and row['Country'] in unicode(name):
                        country = code
                        break

            ci = g.ContactInfo.objects.create(
                user=user,
                phone_number=row['Phone Number'],
                address=row['Address Street'],
                city=row['City'],
                state=row['State'],
                zip=row['Postcode'],
                country=country,
            )

            g.Client.objects.create(
                user=user,
                name=row['Name'],
                email=row['Email'],
                company=row['Organization'] or row['Name'],
                status=g.ClientStatus.Potential.value,
                contact_info=ci,
            )
