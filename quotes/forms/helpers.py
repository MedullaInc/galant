from quotes import models as q
from gallant import models as g
import operator
import re
from section import SectionForm, ServiceForm


def create_quote(quote_form, section_forms):
    obj = quote_form.save(commit=True)
    obj.sections.clear()
    obj.services.clear()

    for s in section_forms:
        if type(s) is SectionForm:
            obj.sections.add(s.save())
        elif type(s) is ServiceForm:
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
                sf.append(ServiceForm(request.user, request.POST, prefix=m.group(1)))

    #sf.sort(key=lambda x: x.index)
    return sf


def section_forms_quote(quote, clear_pk=False):
    sf = []
    for section in quote.all_sections():
        if clear_pk:
            section.pk = None
        if type(section) is q.TextSection:
            sf.append(SectionForm(section.user, instance=section, prefix='-section-%d' % section.index))
        elif type(section) is q.ServiceSection:
            sf.append(ServiceForm(section.user, instance=section, prefix='-service-%d' % section.index))

    return sf


def section_forms_initial(user):
    return [SectionForm(user, instance=q.TextSection(name='intro', index=0), prefix='-section-0'),
            SectionForm(user, instance=q.TextSection(name='important_notes', index=2), prefix='-section-1'),
            ServiceForm(user, instance=q.ServiceSection(name='section_1',
                                                               index=1,
                                                               service=g.Service()),
                               prefix='-service-2')]
