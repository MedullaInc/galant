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


class QuoteStatus(ChoiceEnum):
    DRAFT = 0
    NOT_SENT = 1
    SENT = 2
    VIEWED = 3
    SUPERSEDED = 4  # by a new revision
    ACCEPTED = 5
    REJECTED = 6


class Quote(models.Model):
    intro = models.ForeignKey(Section, null=True, related_name='intro')
    sections = models.ManyToManyField(Section, blank=True)
    notes = models.ForeignKey(Section, null=True, related_name='notes')

    status = models.CharField(max_length=2, choices=QuoteStatus.choices(), default=QuoteStatus.DRAFT.value)
    created = models.DateTimeField(auto_now_add=True)

    token = models.CharField(max_length=64, unique=True, null=True, help_text='For emailing URL')

    parent = models.ForeignKey('self', null=True, blank=True, related_name='versions')