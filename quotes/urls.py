from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from quotes import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'api/quote', views.QuoteViewSet, 'api-quote')
router.register(r'api/quote_template', views.QuoteTemplateViewSet, 'api-quote-template')
router.register(r'api/section', views.SectionViewSet, 'api-section')

urlpatterns = [
    url(r'^$', login_required(views.QuoteList.as_view()), name='quotes'),
    url(r'^add/$', login_required(views.QuoteCreate.as_view()), name='add_quote'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(views.QuoteUpdate.as_view()), name='edit_quote'),
    url(r'^delete/(?P<pk>[0-9]+)$', login_required(views.QuoteDelete.as_view()), name='delete_quote'),
    url(r'^send_quote/(?P<pk>[0-9]+)$', login_required(views.QuoteSend.as_view()), name='send_quote'),
    url(r'^(?P<pk>[0-9]+)?$', login_required(views.QuoteDetail.as_view()), name='quote_detail'),
    url(r'^(?P<token>[a-f0-9]{32})?$', login_required(views.QuoteDetail.as_view()), name='quote_detail'),
    url(r'^template/$', login_required(views.QuoteTemplateList.as_view()), name='quote_templates'),
    url(r'^template/(?P<pk>[0-9]+)?$', login_required(views.QuoteTemplateDetail.as_view()),
        name='quote_template_detail'),
    url(r'^template/add/(?P<quote_id>[0-9]+)?$', login_required(views.QuoteTemplateView.as_view()),
        name='add_quote_template'),
    url(r'^template/edit/(?P<pk>[0-9]+)?$', login_required(views.QuoteTemplateView.as_view()),
        name='edit_quote_template'),
    url(r'^template/delete/(?P<pk>[0-9]+)$', login_required(views.QuoteTemplateDelete.as_view()),
        name='delete_quote_template'),
    url(r'^preview/(?P<pk>[0-9]+)?$', login_required(views.quote_preview), name='quote_preview'),
    url(r'^preview/header/(?P<pk>[0-9]+)?$', login_required(views.quote_header), name='quote_header'),
    url(r'^preview/footer/(?P<pk>[0-9]+)?$', login_required(views.quote_footer), name='quote_footer'),
    url(r'^download/(?P<pk>[0-9]+)?$', login_required(views.QuotePDF.as_view()), name='quote_pdf'),
    url(r'^download/(?P<token>[a-f0-9]{32})?$', login_required(views.QuotePDF.as_view()), name='quote_pdf'),

    url(r'^api/quote/payments/(?P<pk>[0-9]+)$', login_required(views.QuotePaymentsAPI.as_view()),
        name='api_quote_payments'),
]
urlpatterns += router.urls

urlpatterns += url(r'^api/quote/fields',
                   login_required(views.quote_fields_json),
                   name='api-quote-fields'),
