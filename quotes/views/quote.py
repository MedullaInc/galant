from django.http.response import HttpResponse, JsonResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from gallant.utils import get_one_or_404, url_to_pdf, get_site_from_host, GallantObjectPermissions, get_field_choices, \
    GallantViewSetPermissions
from quotes import models as q
from quotes import serializers
from gallant.serializers import payment
from gallant import models as g
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from uuid import uuid4
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED


class QuoteUpdate(View):
    def get(self, request, **kwargs): # pragma: no cover
        self.object = get_one_or_404(request.user, 'change_quote', q.Quote, pk=kwargs['pk'])
        return self.render_to_response({'object': self.object,
                                        'title': 'Edit Quote'})


    def form_valid(self, form, section_forms): # pragma: no cover
        if 'preview' in self.request.POST:  
            form.instance.pk = None
            form.instance.token = uuid4()

            for section_form in section_forms:
                section_form.instance.pk = None
                section_form.instance.id = None

                if hasattr(section_form, 'section'):
                    section_form.section.pk = None
                    section_form.section.id = None

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
            quote.sections.all_for(self.request.user, 'delete').delete()
            quote.services.all_for(self.request.user, 'delete').delete()
            quote.delete()

            return response

        else:
            messages.success(self.request, 'Quote saved.')
            return HttpResponseRedirect(reverse('quote_detail', args=[self.object.id]))

    def render_to_response(self, context): # pragma: no cover
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
            quote.pk = None
            context.update({'template_id': template_id})
            if lang is not None:
                quote.language = lang
                context.update({'language': lang, 'object': quote})

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Add'), request.path_info)])

        return TemplateResponse(request=self.request,
                                template="quotes/quote_form_ng.html",
                                context=context)


def _send_quote_email(email, from_name, link, site): # pragma: no cover
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


# class QuoteDetail(View):
#     def get(self, request, **kwargs):
#         quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['pk'])

#         request.breadcrumbs([(_('Quotes'), reverse('quotes')),
#                              (_('Quote: %s' % quote.name), request.path_info)])
#         return TemplateResponse(request=request,
#                                 template="quotes/quote_detail.html",
#                                 context={'title': 'Quote', 'object': quote})

class QuoteDetail(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['pk'])

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Quote: %s' % quote.name), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quote_detail_ng.html",
                                context={'title': 'Quote', 'object': quote})  

class QuoteSend(View): # pragma: no cover
    def post(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, id=kwargs['pk'])
        quote.status = q.QuoteStatus.Sent.value
        quote.save()

        _send_quote_email(quote.client.email, request.user.name,
                          (request.build_absolute_uri(
                              reverse('quote_pdf', args=[quote.token.hex]))),
                          get_site_from_host(request))
        messages.success(request, 'Quote link sent to %s.' % quote.client.email)
        return HttpResponseRedirect(reverse('quote_detail', args=[quote.id]))


class QuoteList(View):
    def get(self, request):
        self.request.breadcrumbs(_('Quotes'), request.path_info)
        return TemplateResponse(request=request,
                                template="quotes/quote_list_ng.html",
                                context={'title': 'Quotes',
                                         'object_list': q.Quote.objects
                                .all_for(request.user)
                                .filter(client__isnull=False),
                                         'template_list': q.QuoteTemplate.objects
                                .all_for(request.user)})


def quote_fields_json(request):
    return JsonResponse(get_field_choices(q.Quote), safe=False)


class SectionViewSet(ModelViewSet):
    model = q.Section
    serializer_class = serializers.SectionSerializer
    permission_classes = [
         GallantViewSetPermissions
     ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)


class QuoteViewsViewsSet(ModelViewSet):
    model = q.Quote
    serializer_class = serializers.QuoteSerializer
    permission_classes = [
         GallantViewSetPermissions
     ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)    


class QuoteViewSet(ModelViewSet):
    model = q.Quote
    serializer_class = serializers.QuoteSerializer
    permission_classes = [
         GallantViewSetPermissions
     ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)

    def update(self, request, *args, **kwargs):
        response = super(QuoteViewSet, self).update(request, *args, **kwargs)
        if response.status_code == HTTP_200_OK or response.status_code == HTTP_201_CREATED:
            self.request._messages.add(messages.SUCCESS, 'Quote saved.')
            return Response({'status': 0, 'redirect': reverse('quote_detail', args=[response.data['id']])})
        else:
            return response

    def create(self, request, *args, **kwargs):
        response = super(QuoteViewSet, self).create(request, *args, **kwargs)
        if response.status_code == HTTP_201_CREATED:
            self.request._messages.add(messages.SUCCESS, 'Quote saved.')
            return Response({'status': 0, 'redirect': reverse('quote_detail', args=[response.data['id']])})
        else:
            return response

class QuotePaymentsAPI(generics.RetrieveUpdateAPIView):
    model = g.Client
    serializer_class = payment.PaymentSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)
