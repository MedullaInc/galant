# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.utils.translation import activate, get_language
from django.core.urlresolvers import reverse, get_resolver


class SignedOutTest(LiveServerTestCase):
    # fixtures = ['functional_tests/fixtures/ft_one_user.json']

    def setUp(self):
        self.browser = webdriver.PhantomJS()

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # open web browser, go to the admin page
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def test_can_login_int(self):
        language = get_language()
        for lang, e_text in [('en', u'Account Login'),
                                ('es', u'Iniciar Sesión')]:
            activate(lang)
            self.browser.get(self.live_server_url + reverse('home'))
            e = self.browser.find_element_by_css_selector(".login-title")
            self.assertEqual(e.text, e_text)

        activate(language)

    def test_can_signup_int(self):
        language = get_language()
        for lang, e_text in [('en', u'Sign Up Now!'),
                                ('es', u'Regístrate!')]:
            activate(lang)
            self.browser.get(self.live_server_url + reverse('home'))
            e = self.browser.find_element_by_name("signup")
            self.assertEqual(e.text, e_text)

        activate(language)

    def test_page_blocked(self):
        for view_name in get_resolver(None).reverse_dict.keys():
            if hasattr(view_name, '__call__') \
                    or 'account' in view_name \
                    or view_name in ['home']:  # add non-logged in permitted views here
                continue

            # add singe <pk>-requiring views here:
            if view_name in ['edit_client', 'client_detail', 'edit_service', 'service_detail','edit_quote', 'quote_detail', 'edit_quote_template', 'edit_brief', 'client_briefs']:
                url = self.live_server_url + reverse(view_name, args=[0])
            elif view_name in ['add_brief','brief_detail']:
                url = self.live_server_url + reverse(view_name, args=['client', 0])
            else:
                url = self.live_server_url + reverse(view_name)

            self.browser.get(url)

            try:
                h1 = self.browser.find_element_by_tag_name('h1')
            except NoSuchElementException:
                self.fail('h1 Element not found, page is not blocked: %s' %
                          url)

            self.assertIn('Sign In', h1.text)
            self.assertTrue(self.live_server_url + reverse('account_login') in self.browser.current_url)
