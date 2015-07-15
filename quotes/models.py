from gallant import models as g
from gallant import fields as gf
from django.db import models as m
from django.conf import settings
from django.utils.html import escape, mark_safe


# Text section of Quote
class Section(m.Model):
    title = gf.ULCharField()
    text = gf.ULTextField()
    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_sections')

    def render_html(self, language=None):
        html = '<h2 class="section_title">%s</h2><p>%s</p>' % \
               (escape(self.title.get_text(language)), escape(self.text.get_text(language)))
        return mark_safe(html)


class ServiceSection(Section):
    service = m.ForeignKey(g.Service)


class QuoteStatus(gf.ChoiceEnum):
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
    margin_section = m.ForeignKey(Section, null=True, related_name='margin_section',
                                  help_text='This section appears on the margin of the last page of a quote.')

    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of quote, or null for template.')

    status = m.CharField(max_length=2, choices=QuoteStatus.choices(), default=QuoteStatus.Draft.value)
    created = m.DateTimeField(auto_now_add=True)

    token = m.CharField(max_length=64, unique=True, null=True, help_text='For emailing URL')

    parent = m.ForeignKey('self', null=True, blank=True, related_name='versions')


