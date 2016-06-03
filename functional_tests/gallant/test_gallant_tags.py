# -*- coding: utf-8 -*-
from breadcrumbs.breadcrumbs import Breadcrumbs
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.template import Context, Template
from django.test.client import RequestFactory


class TestGallantTags(StaticLiveServerTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_shows_custom_breadcrumb(self):
        request = self.factory.get(self.live_server_url)
        request.breadcrumbs = Breadcrumbs()
        context = {'request': request}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% custom_breadcrumb request "Test" %}', context
        )

        self.assertEqual(rendered, u'')

    def test_shows_active(self):
        request = self.factory.get(self.live_server_url)
        request.breadcrumbs = Breadcrumbs()
        context = {'request': request, 'pattern': self.live_server_url}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% active request pattern %}', context
        )

        self.assertEqual(rendered, u'')

        context = {'request': request, 'pattern': request.path}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% active request pattern %}', context
        )

        self.assertEqual(rendered, u'active')

    def render_template(self, string, context=None):
            context = context or {}
            context = Context(context)
            return Template(string).render(context)
