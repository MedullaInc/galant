import gallant.models as g
import django.db.models as m


class Task(g.UserModel):
    name = m.CharField(max_length=255)
    start = m.DateTimeField(auto_now_add=False)
    end = m.DateTimeField(auto_now_add=False)
    daily_estimate = m.DecimalField(blank=True, default=0.0, decimal_places=1, max_digits=3,
                                    help_text='Time estimate in hours per day')

    project = m.ForeignKey(g.Project, null=True, blank=True)
    services = m.ManyToManyField(g.Service)
    assignee = m.ForeignKey(g.GallantUser, related_name='assignee')
    notes = m.ManyToManyField(g.Note)

    class Meta:
        permissions = (
            ('view_task', 'View task'),
        )

    objects = g.UserModelManager()
