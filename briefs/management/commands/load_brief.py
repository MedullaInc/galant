""" Loads initial quote & brief template, sets group permissions.
"""
from briefs.models import Brief, BriefTemplate, TextQuestion, MultipleChoiceQuestion
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.manager import Manager
from guardian.shortcuts import assign_perm


class Command(BaseCommand):
    help = 'Loads an initial brief template + questions and adds view permissions for "users" group.'

    def handle(self, **kwargs):
        load_brief()


@transaction.atomic
def load_brief():
    UserModel = get_user_model()
    user = UserModel.objects.get(email='AnonymousUser')

    brief = Brief.objects.create(name='Example - Initial Client Questionnaire', user=user,
                                 title={'en': 'Hello!'},
                                 greeting={
                                     'en': 'Please read and complete the following client questionnaire. The more detailed your answers, the better we will be able to understand your needs.'})
    brief_template = BriefTemplate.objects.create(brief=brief, user=user)

    brief.questions.add(
        MultipleChoiceQuestion.objects.create(
            index=0,
            user=user,
            question={'en': 'How did you learn about us?'},
            choices=[{'en': 'I saw a project you developed'}, {'en': 'Search engine'}, {'en': 'Social media'},
                     {'en': 'Your firm reached out'}, {'en': 'Recommendation'}]
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=1,
            user=user,
            question={'en': 'What is your line of business?'}
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=2,
            user=user,
            question={'en': 'What\'s your company\'s name? (Leave blank if you don\'t have one.)'}
        )
    )

    brief.questions.add(
        MultipleChoiceQuestion.objects.create(
            index=3,
            user=user,
            question={'en': 'What is the size of your business?'},
            choices=[{'en': 'Micro'}, {'en': 'Small'}, {'en': 'Medium'}, {'en': 'Large'}]
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=4,
            user=user,
            question={'en': 'Why is your company interested in our services?'}
        )
    )

    brief.questions.add(
        MultipleChoiceQuestion.objects.create(
            index=5,
            user=user,
            question={'en': 'How long has this company existed?'},
            choices=[{'en': 'New company'}, {'en': 'Recently created (1 year or less)'}, {'en': '1-5 years'},
                     {'en': 'More than 5 years'}]
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=6,
            user=user,
            is_long_answer=True,
            question={'en': 'Describe the products or services that your company offers.'}
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=7,
            user=user,
            is_long_answer=True,
            question={'en': 'Describe your sales process in detail.'}
        )
    )

    brief.questions.add(
        MultipleChoiceQuestion.objects.create(
            index=8,
            user=user,
            can_select_multiple=True,
            question={'en': 'What services are you expecting to receive from us?'},
            choices=[{'en': 'Identity (Logo)'}, {'en': 'Naming'},
                     {'en': 'Stationery  (business cards, letterhead, invoices, etc)'},
                     {'en': 'Sales items ( brochure, flyers, presentations, etc )'},
                     {'en': 'Establishment items ( uniforms, signage, menus, etc )'},
                     {'en': 'Packaging ( labels, boxes, bags, bottles, etc )'},
                     {'en': 'Advertisement ( press advertisements, billboards, etc )'},
                     {'en': 'Web design & development ( corporate websites, operational tools )'},
                     {'en': 'Interiors ( architecture and distribution, interior design, furniture, construction )'},
                     {'en': 'Other'}]
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=9,
            user=user,
            is_long_answer=True,
            question={'en': 'What specific deliverables do you expect from us?'}
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=10,
            user=user,
            question={'en': 'Which brands would you consider aspirational for your business?'}
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=11,
            user=user,
            question={'en': 'What\'s your project budget, if you have one?'}
        )
    )

    brief.questions.add(
        TextQuestion.objects.create(
            index=12,
            user=user,
            question={'en': 'Is there a calendar deadline for this project? If so, what is it?'}
        )
    )

    set_brief_perms(brief_template)


def set_brief_perms(brief_template):
    users_group = Group.objects.get(name='users')

    brief = brief_template.brief

    assign_perm('view_brieftemplate', users_group, brief_template)
    assign_perm('view_brief', users_group, brief)

    for s in super(Manager, brief.questions).all():
        assign_perm('view_question', users_group, s)
