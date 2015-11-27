from django.db import models as m


class CustomerLead(m.Model):
    name = m.CharField(blank=False, max_length=255)
    email = m.EmailField(unique=True)
    website = m.URLField(blank=True)
