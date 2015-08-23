from django.http.response import HttpResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from gallant.utils import get_one_or_404, url_to_pdf
from moneyed import Money
from quotes import models as q
from quotes import forms as qf
from gallant import forms as gf
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


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

        form = qf.QuoteForm(request.user, request.POST, instance=self.object)
        section_forms = qf.section_forms_request(request)

        valid = list([form.is_valid()] + [s.is_valid() for s in section_forms])

        if all(valid):
            if 'preview' in request.POST:
                quote = form.save(commit=False)
                sections = []

                for section_form in section_forms:
                    sections.append(section_form.save(commit=False))

                total_cost = Money(0, "USD")

                for section in sections:
                    if hasattr(section, 'service'):
                        total_cost += section.service.get_total_cost()

                context = {'object': quote, 'sections': sections, 'total_cost': total_cost}

                return TemplateResponse(request, template="quotes/quote_preview_html.html", context=context)

            else:
                return self.form_valid(form, section_forms)

        else:
            return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms,
                                            'title': 'Edit Quote'})

    def form_valid(self, form, section_forms):
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


class QuoteDetail(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['pk'])

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Quote: %s' % quote.name), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quote_detail.html",
                                context={'title': 'Quote', 'object': quote})


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


class QuoteTemplateList(View):
    def get(self, request):
        self.request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                                  (_('Templates'), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quotetemplate_list.html",
                                context={'title': 'Quote Templates',
                                         'object_list': q.QuoteTemplate.objects
                                .all_for(request.user, 'view_quotetemplate')})


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        self.request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                                  (_('Templates'), reverse('quote_templates'))])

        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])
            form = qf.QuoteTemplateForm(request.user, instance=self.object.quote)
            section_forms = qf.section_forms_quote(self.object.quote)

            if not request.user.has_perm('change_quotetemplate', self.object):
                messages.warning(request, 'Warning: you don\'t have permission to change this template. '
                                 'To save it as your own, use it to create a quote, then '
                                 'create a separate template from the new quote.')

            self.request.breadcrumbs([(_('Edit'), request.path_info)])
        else:
            self.object = None
            self.request.breadcrumbs([(_('Add'), request.path_info)])

            if kwargs['quote_id'] is not None:
                quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['quote_id'])
                form = qf.QuoteTemplateForm(request.user, instance=quote)
                section_forms = qf.section_forms_quote(quote)
            else:
                form = qf.QuoteTemplateForm(request.user)
                section_forms = qf.section_forms_initial(request.user)

        return self.render_to_response({'form': form, 'sections': section_forms}, request)

    def post(self, request, **kwargs):
        section_forms = qf.section_forms_request(request)
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])
            form = qf.QuoteTemplateForm(request.user, request.POST, instance=self.object.quote)
        else:
            self.object = None
            form = qf.QuoteTemplateForm(request.user, request.POST)

        valid = list([form.is_valid()] + [s.is_valid() for s in section_forms])
        if all(valid):
            return self.form_valid(form, section_forms)
        else:
            return self.render_to_response({'form': form, 'sections': section_forms}, request)

    def form_valid(self, form, section_forms):
        quote = qf.create_quote(form, section_forms)
        if hasattr(self, 'object') and self.object is None:
            self.object = q.QuoteTemplate.objects.create(user=quote.user, quote=quote)
        messages.success(self.request, 'Template saved.')
        return HttpResponseRedirect(reverse('edit_quote_template', args=[self.object.id]))

    def render_to_response(self, context, request):
        lang_dict = dict(settings.LANGUAGES)
        form = gf.LanguageForm()
        language_set = set()
        language = get_language()

        if hasattr(self.object, 'quote'):  # TODO: move this block out of here / remove request param
            language_set.update(self.object.quote.get_languages())
            quote = self.object.quote
            context.update({'title': 'Edit Template'})
        elif 'quote_id' in self.kwargs and self.kwargs['quote_id'] is not None:
            quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=self.kwargs['quote_id'])
            context.update({'title': 'New Template'})
        else:
            quote = q.Quote()
            context.update({'title': 'New Template'})

        if language_set:
            language = next(iter(language_set))
        else:
            language_set.add(language)
        context.update({'languages': [(c, lang_dict[c]) for c in language_set if c in lang_dict],
                        'language_form': form,
                        'object': quote,
                        'template': self.object,
                        'language': language,
                        'quote_type': 'template'})
        return TemplateResponse(request=self.request,
                                template="quotes/quote_template.html",
                                context=context)


class QuotePDF(View):  # pragma: no cover
    def get(self, request, *args, **kwargs):
        quote = q.Quote.objects.get_for(request.user, 'view_quote', pk=kwargs['pk'])
        url = '%s://%s%s' % (request.scheme, request.get_host(), reverse('quote_preview', args=[quote.id]))
        filename = slugify(quote.client.name + "_" + quote.name)
        # load page with ?dl=inline to show PDF in browser
        attach_or_inline = request.GET.get('dl', 'inline')

        pdf = url_to_pdf(url, request.session.session_key)

        response = HttpResponse(content=pdf,
                                content_type='application/pdf')
        # change 'attachment' to 'inline' to display in page rather than d/l
        response['Content-Disposition'] = '%s; filename="%s.pdf"' % (attach_or_inline, filename)
        return response


def quote_preview_html(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.get_for(request.user, 'view_quote', pk=kwargs['pk'])

    # Render HTML
    context = {'object': quote}
    return TemplateResponse(request, template="quotes/quote_preview_html.html", context=context)


def quote_preview(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.get_for(request.user, 'view_quote', pk=kwargs['pk'])

    # Render HTML
    context = {'object': quote}
    return TemplateResponse(request, template="quotes/quote_preview.html", context=context)
