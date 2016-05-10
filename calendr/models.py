import gallant.models as g
import django.db.models as m
from django.db.models.signals import post_save
from django.dispatch import receiver
from gallant import fields as gf


class TaskStatus(gf.ChoiceEnum):
    """ Determines Client's place in workflow / pipeline.
    """
    ToDo = 0
    Ready = 1
    In_Progress = 2
    Done = 3


class Task(g.UserModel):
    name = m.CharField(max_length=255)
    start = m.DateTimeField(auto_now_add=False)
    end = m.DateTimeField(auto_now_add=False)
    daily_estimate = m.DecimalField(blank=True, default=0.0, decimal_places=1, max_digits=3,
                                    help_text='Time estimate in hours per day')
    status = m.CharField(max_length=2, choices=TaskStatus.choices(), default=TaskStatus.ToDo.value)

    project = m.ForeignKey(g.Project, null=True, blank=True)
    services = m.ManyToManyField(g.Service)
    assignee = m.ForeignKey(g.GallantUser, related_name='assignee')
    notes = m.ManyToManyField(g.Note)

    class Meta:
        permissions = (
            ('view_task', 'View task'),
        )

    objects = g.UserModelManager()


@receiver(post_save, sender=Task)
def deliverable_in_progress(sender, instance, **kwargs):
    if instance.services.all_for(instance.user):
        for service in instance.services.all_for(instance.user):
            if service.status == "1" and instance.status == "2":
                service.status = "2"
                service.save()