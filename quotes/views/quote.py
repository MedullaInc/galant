from django.http.response import HttpResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from gallant.utils import get_one_or_404, url_to_pdf, get_site_from_host
from quotes import models as q
from quotes import forms as qf
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from uuid import uuid4


class QuoteUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_quote', q.Quote, pk=kwargs['pk'])
        form = qf.QuoteForm(request.user, instance=self.object)
        section_forms = qf.section_forms_quote(quote=self.object)
        return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms,
                                        'title': 'Edit Quote'})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_quote', q.Quote, pk=kwargs['pk'])
        else:
            self.object = None

        if 'preview' in self.request.POST:
            self.object.project_id = None

        form = qf.QuoteForm(request.user, request.POST, instance=self.object)
        section_forms = qf.section_forms_request(request)

        valid = list([form.is_valid()] + [s.is_valid() for s in section_forms])

        if all(valid):
            return self.form_valid(form, section_forms)

        else:
            return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms,
                                            'title': 'Edit Quote'})

    def form_valid(self, form, section_forms):
        if 'preview' in self.request.POST:  # pragma: no cover
            form.instance.pk = None
            form.instance.token = uuid4()

            for section_form in section_forms:
                section_form.instance.pk = None
                section_form.instance.id = None

                if hasattr(section_form, 'section'):
                    section_form.section.pk = None
                    section_form.section.id = None

            self.object = qf.create_quote(form, section_forms)

            quote = self.object
            url = '%s://%s%s' % (
            self.request.scheme, self.request.get_host(), reverse('quote_preview', args=[quote.id]))
            filename = slugify(quote.client.name + "_" + quote.name)

            attach_or_inline = 'inline'

            header_url = url.replace('preview', 'preview/header')
            footer_url = url.replace('preview', 'preview/footer')  # .replace(':8000', ':8001')

            pdf = url_to_pdf(url, self.request.session.session_key, header_url, footer_url)

            response = HttpResponse(content=pdf, content_type='application/pdf')

            response['Content-Disposition'] = '%s; filename="%s.pdf"' % (attach_or_inline, filename)

            # Delete preview quote / services / sections
            quote.sections.all_for(self.request.user, 'delete_section').delete()
            quote.services.all_for(self.request.user, 'delete_section').delete()
            quote.delete()

            return response

        else:
            self.object = qf.create_quote(form, section_forms)
            messages.success(self.request, 'Quote saved.')
            return HttpResponseRedirect(reverse('quote_detail', args=[self.object.id]))

    def render_to_response(self, context):
        self.request.breadcrumbs(_('Quotes'), reverse('quotes'))
        if self.object:
            self.request.breadcrumbs([(_('Quote: %s' % self.object.name),
                                       reverse('quote_detail', args=[self.object.id])),
                                      (_('Edit'), self.request.path_info)])
        else:
            self.request.breadcrumbs(_('Add'), self.request.path_info)

        return TemplateResponse(request=self.request,
                                template="quotes/quote_form.html",
                                context=context)


class QuoteCreate(QuoteUpdate):
    def get(self, request):
        context = {'title': 'Add Quote'}
        template_id = request.GET.get('template_id', None)
        lang = request.GET.get('lang', None)
        if template_id is not None:
            template = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=template_id)
            quote = template.quote
            section_forms = qf.section_forms_quote(quote, clear_pk=True)
            context.update({'sections': section_forms})
            quote.pk = None
            if lang is not None:
                quote.language = lang
                context.update({'language': lang, 'form': qf.QuoteForm(request.user, instance=quote), 'object': quote})
        else:
            context.update({'form': qf.QuoteForm(request.user, instance=q.Quote()),
                            'sections': qf.section_forms_initial(request.user)})

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Add'), request.path_info)])

        return TemplateResponse(request=self.request,
                                template="quotes/quote_form.html",
                                context=context)


def _send_quote_email(email, from_name, link, site):
    message = '%s has sent you a Quote from %s.\n\n Click this link to view:\n %s' % \
              (from_name, site, link)
    send_mail('Client Quote', message,
              '%s via %s <%s>' % (from_name, site, settings.EMAIL_HOST_USER),
              [email], fail_silently=False)


class QuoteDelete(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'change_quote', q.Quote, id=kwargs['pk'])
        quote.soft_delete()

        return HttpResponseRedirect(reverse('quotes'))


class QuoteTemplateDelete(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'change_quotetemplate', q.QuoteTemplate, id=kwargs['pk'])
        quote.soft_delete()

        return HttpResponseRedirect(reverse('quote_templates'))


class QuoteDetail(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['pk'])

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Quote: %s' % quote.name), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quote_detail.html",
                                context={'title': 'Quote', 'object': quote})

    def post(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, id=kwargs['pk'])
        quote.status = q.QuoteStatus.Sent.value
        quote.save()

        _send_quote_email(quote.client.email, request.user.name,
                          (request.build_absolute_uri(
                              reverse('quote_pdf', args=[quote.token.hex]))),
                          get_site_from_host(request))
        messages.success(request, 'Quote link sent to %s.' % quote.client.email)
        return self.get(request, **kwargs)


class QuoteList(View):
    def get(self, request):
        self.request.breadcrumbs(_('Quotes'), request.path_info)
        return TemplateResponse(request=request,
                                template="quotes/quote_list.html",
                                context={'title': 'Quotes',
                                         'object_list': q.Quote.objects
                                .all_for(request.user, 'view_quote')
                                .filter(client__isnull=False),
                                         'template_list': q.QuoteTemplate.objects
                                .all_for(request.user, 'view_quotetemplate')})