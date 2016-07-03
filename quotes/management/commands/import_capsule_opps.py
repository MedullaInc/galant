from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from gallant import models as g
from moneyed.classes import Money
from quotes import models as q
import django_countries
import csv

class Command(BaseCommand):
    help = 'Loads a CSV from Capsule opportunities export.'

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
            client = None
            cs = list(g.Client.objects.all_for(user).filter(company=row['Contact Name']))
            if cs:
                client = cs[0]
            else:
                cs = list(g.Client.objects.all_for(user).filter(name=row['Contact Name']))
                if cs:
                    client = cs[0]

            if row['Duration Basis'] == 'month':
                name = 'Monthly Service'
            elif row['Duration Basis'] == 'hour':
                name = 'Hourly Service'
            elif row['Duration Basis'] == 'fixed':
                name = 'Fixed Rate Service'

            service = g.Service.objects.create(
                user=user,
                name=name,
                description=row['Opportunity Description'],
                cost=Money(row['Value per Duration'] or 0, row['Currency'] or 'USD'),
                quantity=row['Duration'] or 0,
            )

            status = q.QuoteStatus.Not_Sent.value
            pstatus = g.ProjectStatus.Pending_Assignment.value
            if 'Customer' in row['Milestone']:
                status = q.QuoteStatus.Accepted.value
                if 'In Progress' in row['Milestone']:
                    pstatus = g.ProjectStatus.Active.value
                elif 'Closed' in row['Milestone']:
                    pstatus = g.ProjectStatus.Completed
            elif row['Milestone'] == 'Opportunity - Proposal' or \
                    row['Milestone'] == 'Paused':
                status = q.QuoteStatus.Sent.value
                if row['Milestone'] == 'Paused':
                    pstatus = g.ProjectStatus.On_Hold.value
            elif row['Milestone'] == 'Lost':
                status = q.QuoteStatus.Rejected.value

            quote = q.Quote.objects.create(
                user=user,
                name=row['Opportunity Name'],
                status=status,
                client=client,
            )

            quote.services.add(service)

            if pstatus != g.ProjectStatus.Pending_Assignment.value:
                project = g.Project.objects.create(
                    user=user,
                    name=quote.name,
                    client=client,
                )

                service.pk = None
                service.save()

                project.services.add(service)
