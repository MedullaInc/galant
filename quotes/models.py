from django.db import models
from gallant.models import *
from django.utils.html import escape, mark_safe


# Text section of Quote
class Section(models.Model):
    title = models.ForeignKey(ULText, related_name='title')
    text = models.ForeignKey(ULText, related_name='text')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_sections')

    def render_html(self, language=None):
        html = '<h1>%s</h1><br>%s' % (escape(self.title.get_text(language)), escape(self.text.get_text(language)))
        return mark_safe(html)


class ServiceSection(Section):
    service = models.ForeignKey(Service)


class Quote(models.Model):
    intro = models.ForeignKey(Section)