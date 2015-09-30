from gallant.utils import get_one_or_404
from quotes import models as q
from gallant import models as g
from gallant import forms as gf
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template


class SectionForm(gf.UserModelForm):
    class Meta:
        model = q.TextSection
        fields = ['name', 'title', 'text', 'index']

    def __init__(self, user, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            section = get_one_or_404(user, 'change_textsection',
                                     q.TextSection, pk=data[prefix + '-id'])
            super(SectionForm, self).__init__(user, data=data, prefix=prefix, instance=section, *args, **kwargs)
        else:
            super(SectionForm, self).__init__(user, data=data, prefix=prefix, *args, **kwargs)

        self.index = self.instance.index

    def as_table(self):
        t = get_template('quotes/section_form.html')
        if self.instance:
            section = self.instance
        else:
            section = self.save(commit=False)
        context = {'prefix': self.prefix + '-', 'name': section.name,
                   'section': section, 'form': self}

        if section.name == 'margin':
            context.update({'help_text': _('This section appears last, in the margin of the final page.')})
        elif section.name == 'intro':
            context.update({'help_text': _('This section appears first, with special formatting.')})
        else:
            context.update({'extra_class': 'dynamic_section'})
        return t.render(context)


class ServiceSectionForm(gf.UserModelForm):
    class Meta:
        model = g.Service  # make sure to call with ServiceSection instance, not Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']

    def __init__(self, user, data=None, instance=None, *args, **kwargs):
        super(ServiceSectionForm, self).__init__(user=user, data=data, instance=instance, *args, **kwargs)
        self.section = None

        # check to see if we were called with an instance param
        if instance:
            self.section = instance
            self.instance = self.section.service
        elif self.prefix + '-id' in self.data:
            self.section = get_one_or_404(user, 'change_servicesection',
                                          q.ServiceSection, pk=self.data[self.prefix + '-id'])
            self.instance = self.section.service
        else:
            name = self.data[self.prefix + '-section_name']
            index = self.data[self.prefix + '-index']
            self.section = q.ServiceSection(user=user, name=name, index=index)
        self.index = self.section.index

    def as_table(self):
        t = get_template('quotes/service_section_form.html')

        return t.render({'prefix': self.prefix + '-', 'section': self.section,
                         'type_choices': g.ServiceType.choices(), 'form': self,
                         'extra_class': 'dynamic_section'})

    def save(self, commit=True):
        super(ServiceSectionForm, self).save(commit)
        self.section.service = self.instance

        if commit:
            self.section.save()
        return self.section
