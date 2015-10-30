from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from briefs import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'api/brief', views.BriefViewSet, 'api-brief')

urlpatterns = [
    url(r'^$', login_required(views.BriefList.as_view()), name='briefs'),
    url(r'^answer/(?P<token>[a-f0-9]{32})$', views.BriefAnswer.as_view(), name='brief_answer'),
    url(r'^add/$', login_required(views.BriefCreate.as_view()), name='add_brief'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(views.BriefUpdate.as_view()), name='edit_brief'),
    url(r'^delete/(?P<pk>[0-9]+)$', login_required(views.BriefDelete.as_view()), name='delete_brief'),
    url(r'^(?P<pk>[0-9]+)?$', login_required(views.BriefDetail.as_view()), name='brief_detail'),
    url(r'^template/$', login_required(views.BriefTemplateList.as_view()), name='brief_templates'),
    url(r'^template/(?P<pk>[0-9]+)?$', login_required(views.BriefTemplateDetail.as_view()), name='brief_template_detail'),
    url(r'^template/add/(?P<brief_id>[0-9]+)?$', login_required(views.BriefTemplateView.as_view()), name='add_brief_template'),
    url(r'^template/edit/(?P<pk>[0-9]+)$', login_required(views.BriefTemplateView.as_view()), name='edit_brief_template'),
    url(r'^template/delete/(?P<pk>[0-9]+)$', login_required(views.BriefTemplateDelete.as_view()),name='delete_brief_template'),

    url(r'^api/template/(?P<pk>[0-9]+)$', login_required(views.BriefTemplateDetailAPI.as_view()), name='api_brief_template_detail'),
    url(r'^api/question/(?P<pk>[0-9]+)$', login_required(views.QuestionDetailAPI.as_view()), name='api_question_detail'),
    url(r'^api/questions/$', login_required(views.QuestionsAPI.as_view()), name='api_questions'),
]

urlpatterns += router.urls
