from gallant import models as g
from gallant import fields as gf
from django.db import models as m
from django.conf import settings
from django.utils.html import escape, mark_safe
from itertools import chain
from gallant import utils


# Text section of Quote
class Section(m.Model):
    name = m.CharField(max_length=256, default="section")
    title = gf.ULCharField()
    text = gf.ULTextField()
    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_sections')

    def render_html(self, language=None):
        html = '<h2 class="section_title">%s</h2><p>%s</p>' % \
               (escape(self.title.get_text(language)), escape(self.text.get_text(language)))
        return mark_safe(html)

    def display_title(self):
        return self.name.replace('_', ' ').title()

    def get_languages(self):
        language_set = set()
        map(lambda l: language_set.add(l), self.title.keys())
        map(lambda l: language_set.add(l), self.text.keys())
        return language_set


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

    def get_languages(self):
        language_set = set()
        for s in list(chain([self.intro], [self.margin_section], self.sections.all())):
            if s is not None:
                language_set.update(s.get_languages())

        return language_set

    def all_sections(self):
        intro = self.intro if self.intro is not None else Section(name='intro')
        margin_section = self.margin_section if self.margin_section is not None else Section(name='margin_section')
        sections = self.sections.all() if self.pk is not None else []

        return list(chain([intro], [margin_section], sections))


class QuoteTemplate(m.Model):
    quote = m.ForeignKey(Quote)

    def language_list(self):
        return [(c,utils.LANG_DICT[c]) for c in self.quote.get_languages() if c in utils.LANG_DICT]