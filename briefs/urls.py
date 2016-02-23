from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from briefs import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'api/brief', views.BriefViewSet, 'api-brief')
router.register(r'api/briefanswers', views.BriefAnswersViewSet, 'api-briefanswers')
router.register(r'api/template', views.BriefTemplateViewSet, 'api-brief-template')

urlpatterns = [
    url(r'^$', login_required(views.BriefList.as_view()), name='briefs'),
    url(r'^answer/(?P<token>[a-f0-9]{32})$', views.BriefAnswer.as_view(), name='brief_answer'),
    url(r'^add/$', login_required(views.BriefDetail.as_view()), name='add_brief'),

    url(r'^(?P<pk>[0-9]+)?$', login_required(views.BriefDetail.as_view()), name='brief_detail'),
    url(r'^template/$', login_required(views.BriefTemplateList.as_view()), name='brieftemplates'),
    url(r'^template/(?P<pk>[0-9]+)?$', login_required(views.BriefTemplateDetail.as_view()), name='brieftemplate_detail'),
    url(r'^template/add/(?P<brief_id>[0-9]+)?$', login_required(views.BriefTemplateDetail.as_view()), name='add_brief_template'),

    url(r'^api/question/(?P<pk>[0-9]+)$', login_required(views.QuestionDetailAPI.as_view()), name='api_question_detail'),
    url(r'^api/questions/$', login_required(views.QuestionsAPI.as_view()), name='api_questions'),
]

urlpatterns += router.urls
