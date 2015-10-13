from django.http.response import HttpResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from gallant.utils import url_to_pdf
from django.shortcuts import get_object_or_404
from quotes import models as q
from django.utils.text import slugify


class QuotePDF(View):  # pragma: no cover
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Quote for a logged-in user
            quote = q.Quote.objects.get_for(request.user, pk=kwargs['pk'])
        elif 'token' in kwargs:
            # Quote for visitor directly from url with token
            quote = get_object_or_404(q.Quote, token=kwargs['token'])

        url = '%s://%s%s' % (request.scheme, request.get_host(), reverse('quote_preview', args=[quote.id]))
        filename = slugify(quote.client.name + "_" + quote.name)

        # load page with ?dl=inline to show PDF in browser
        attach_or_inline = request.GET.get('dl', 'inline')

        header_url = url.replace('preview', 'preview/header')
        footer_url = url.replace('preview', 'preview/footer')  # .replace(':8000', ':8001')

        pdf = url_to_pdf(url, request.session.session_key, header_url, footer_url)

        response = HttpResponse(content=pdf,
                                content_type='application/pdf')

        # change 'attachment' to 'inline' to display in page rather than d/l
        response['Content-Disposition'] = '%s; filename="%s.pdf"' % (attach_or_inline, filename)

        return response


def quote_preview(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.get_for(request.user, pk=kwargs['pk'])

    # Render HTML
    context = {'object': quote}
    return TemplateResponse(request, template="quotes/quote_preview.html", context=context)


def quote_header(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.get_for(request.user, pk=kwargs['pk'])

    # Render HTML
    context = {'object': quote}
    return TemplateResponse(request, template="quotes/quote_header.html", context=context)


def quote_footer(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.get_for(request.user, pk=kwargs['pk'])

    # Render HTML
    context = {'object': quote}
    return TemplateResponse(request, template="quotes/quote_footer.html", context=context)
