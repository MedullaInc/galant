from gallant import models as g
from django.db import models as m
from django.conf import settings
from django.utils.html import escape, mark_safe


# Text section of Quote
class Section(m.Model):
    title = m.ForeignKey(g.ULText, related_name='title')
    text = m.ForeignKey(g.ULText, related_name='text')
    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_sections')

    def render_html(self, language=None):
        html = '<h1>%s</h1><br>%s' % (escape(self.title.get_text(language)), escape(self.text.get_text(language)))
        return mark_safe(html)


class ServiceSection(Section):
    service = m.ForeignKey(g.Service)


class QuoteStatus(g.ChoiceEnum):
    Draft = 0
    Not_Sent = 1
    Sent = 2
    Viewed = 3
    Superseded = 4  # by a new revision
    Accepted = 5
    Rejected = 6


class Quote(m.Model):
    name = m.CharField(max_length=512, default='New Quote')
    client = m.ForeignKey(g.Client, null=True)
    intro = m.ForeignKey(Section, null=True, related_name='intro')
    sections = m.ManyToManyField(Section, blank=True)
    notes = m.ForeignKey(Section, null=True, related_name='notes')

    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                         help_text='Language of quote, or null for template.')

    status = m.CharField(max_length=2, choices=QuoteStatus.choices(), default=QuoteStatus.Draft.value)
    created = m.DateTimeField(auto_now_add=True)

    token = m.CharField(max_length=64, unique=True, null=True, help_text='For emailing URL')

    parent = m.ForeignKey('self', null=True, blank=True, related_name='versions')


