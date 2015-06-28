from django.db import models
from gallant.models import ULText


# Text section of Quote
class Section(models.Model):
    title = models.ForeignKey(ULText, related_name='title')
    text = models.ForeignKey(ULText, related_name='text')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_sections')

    def render_html(self, language=None):
        html = '<h1>%s</h1><br>%s' % (self.title.get_text(language), self.text.get_text(language))
        return html


class Quote(models.Model):
    intro = models.ForeignKey(Section)