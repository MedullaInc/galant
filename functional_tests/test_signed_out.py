# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from selenium import webdriver
from django.utils.translation import activate

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
        for lang, e_text in [('en', u'Account Login'),
                                ('es', u'Iniciar Sesión')]:
            activate(lang)
            self.browser.get(self.live_server_url + '/%s/' % lang)
            e = self.browser.find_element_by_css_selector(".login-title")
            self.assertEqual(e.text, e_text)

    def test_can_signup_int(self):
        for lang, e_text in [('en', u'Sign Up Now!'),
                                ('es', u'Regístrate!')]:
            activate(lang)
            self.browser.get(self.live_server_url + '/%s/' % lang)
            e = self.browser.find_element_by_name("signup")
            self.assertEqual(e.text, e_text)
