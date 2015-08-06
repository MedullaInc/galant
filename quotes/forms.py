from django.core.exceptions import ValidationError
from gallant.utils import get_one_or_404
from quotes import models as q
from gallant import models as g
from gallant import forms as gf
from django.template.loader import get_template
import operator
import re


class QuoteForm(gf.UserModelForm):
    class Meta:
        model = q.Quote
        fields = ['name', 'client', 'status']

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = g.Client.objects.all_for(self.user, 'view_client')

    def clean_client(self):
        client = self.cleaned_data['client']
        if self.user.has_perm('view_client', client):
            return client
        else:
            raise ValidationError('Invalid client.')


class QuoteTemplateForm(gf.UserModelForm):
    class Meta:
        model = q.Quote
        fields = ['name']


def create_quote(quote_form, section_forms):
    obj = quote_form.save(commit=True)
    obj.sections.clear()
    obj.services.clear()

    for s in section_forms:
        if type(s) is SectionForm:
            obj.sections.add(s.save())
        elif type(s) is ServiceSectionForm:
            obj.services.add(s.save())

    obj.save()
    return obj


def section_forms_request(request):
    sf = []
    for key, value in sorted(request.POST.items(), key=operator.itemgetter(1)):
        m = re.match('(-section-\d+)-name', key)
        if m is not None:
            sf.append(SectionForm(request.user, request.POST, prefix=m.group(1)))
        else:
            m = re.match('(-service-\d+)-name', key)
            if m is not None:
                sf.append(ServiceSectionForm(request.user, request.POST, prefix=m.group(1)))

    sf.sort(key=lambda x: x.index)
    return sf


def section_forms_quote(quote, clear_pk=False):
    sf = []
    for section in quote.all_sections():
        if clear_pk:
            section.pk = None
        if type(section) is q.TextSection:
            sf.append(SectionForm(section.user, instance=section, prefix='-section-%d' % section.index))
        elif type(section) is q.ServiceSection:
            sf.append(ServiceSectionForm(section.user, instance=section, prefix='-service-%d' % section.index))

    return sf


def section_forms_initial(user):
    return [SectionForm(user, instance=q.TextSection(name='intro', index=0), prefix='-section-0'),
            SectionForm(user, instance=q.TextSection(name='margin', index=1), prefix='-section-1')]


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
        if section.name != 'margin' and section.name != 'intro':
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

        self.section.save()
        return self.section
