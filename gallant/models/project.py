from django.db import models as m
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from gallant import fields as gf
from . import ClientStatus
from gallant_user import UserModel, UserModelManager
from misc import Note


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

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            for note in self.notes.all_for(self.user, 'change'):
                note.soft_delete(deleted_by_parent=True)

            super(Project, self).soft_delete(deleted_by_parent)


@receiver(post_save, sender=Project)
def client_project(sender, instance, **kwargs):
    for quote in instance.quote_set.all_for(instance.user).filter(client__isnull=False).select_related('client'):
        client = quote.client
        cstat = int(client.status)

        if client.auto_pipeline and cstat < ClientStatus.Project_Underway.value:
            client.status = ClientStatus.Project_Underway.value
            cstat = client.status
            client.alert = ''
            client.save()

        if cstat == ClientStatus.Project_Underway.value:
            set_client_project_alert(client, instance.user)

            if client.auto_pipeline:
                check_and_close(client, instance.user)

            client.save()


def set_client_project_alert(client, user):
    """ Order projects for client by status importance and set alerts
    """
    top_status = Project.objects.all_for(user).filter(quote__client=client)\
                        .exclude(status=ProjectStatus.Completed.value).exclude(status=ProjectStatus.Active.value)\
                        .order_by('-status').values('status').distinct()[:1]

    if top_status:
        pstat = int(top_status[0]['status'])

        if pstat == ProjectStatus.Overdue.value:
            client.alert = 'Project Overdue'
        elif pstat == ProjectStatus.Pending_Assignment.value:
            client.alert = 'Project Pending Assignment'
        elif pstat == ProjectStatus.On_Hold.value:
            client.alert = 'Project On Hold'
    else:
        client.alert = ''


def check_and_close(client, user):
    if Project.objects.all_for(user).filter(quote__client=client)\
                                       .exclude(status=ProjectStatus.Completed.value).count() == 0:
        client.status = ClientStatus.Closed.value
