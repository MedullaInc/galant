from gallant.utils import get_one_or_404
from quotes import models as q
from gallant import models as g
from gallant import forms as gf
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template


class ServiceForm(gf.UserModelForm):
    class Meta:
        model = g.Service  # make sure to call with ServiceSection instance, not Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']

    def __init__(self, user, data=None, instance=None, *args, **kwargs):
        super(ServiceForm, self).__init__(user=user, data=data, instance=instance, *args, **kwargs)
        self.service = None

        # check to see if we were called with an instance param
        if instance:
            self.service = instance
            self.instance = self.service
        elif self.prefix + '-id' in self.data:
            self.service = get_one_or_404(user, 'change_service',
                                          g.Service, pk=self.data[self.prefix + '-id'])
            self.instance = self.service
        else:
            name = self.data[self.prefix]
            index = self.data[self.prefix + '-index']
            quantity = self.data[self.prefix + '-quantity']
            self.service = g.Service(user=user, name=name, quantity=quantity)
        #self.index = self.section.index

    def as_table(self):
        t = get_template('quotes/service_section_form.html')

        return t.render({'prefix': self.prefix + '-', 'section': self.section,
                         'type_choices': g.ServiceType.choices(), 'form': self,
                         'extra_class': 'dynamic_section'})

    def save(self, commit=True):
        super(ServiceForm, self).save(commit)
        self.section.service = self.instance

        if commit:
            self.section.save()
        return self.section
