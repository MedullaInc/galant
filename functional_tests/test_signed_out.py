# -*- coding: utf-8 -*-
import time
from unittest.case import skip
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
        for lang, e_text in [('en', u'Get organized.'),
                             #('es', u'Regístrate!')
                             ]:
            activate(lang)
            self.browser.get(self.live_server_url + reverse('home'))
            e = self.browser.find_element_by_name("signup")
            self.assertEqual(e.text, e_text)

        activate(language)

    def test_page_blocked(self):
        for view_name in get_resolver(None).reverse_dict.keys():
            # add non-logged in permitted views here:
            if hasattr(view_name, '__call__') \
                    or 'account' in view_name \
                    or view_name in ['home', 'brief_answer', 'signup', 'contact', 'register',
                                     'feedback']:
                continue

            # add single <pk>-requiring views here:
            if view_name in ['edit_client', 'client_detail', 'add_service', 'edit_quote',
                             'quote_detail', 'edit_quote_template', 'client_briefs', 'brief_list', 'edit_brief',
                             'brief_detail', 'edit_project', 'project_detail', 'add_project', 'delete_client',
                             'delete_quote', 'delete_brief_template', 'delete_brief', 'edit_brief_template',
                             'delete_quote_template', 'delete_project', 'api_service_detail', 'api_task_detail',
                             'api_project_detail', 'api_client_detail', 'api_note_detail', 'api_quote_detail',
                             'api_quote_template_detail', 'api_brief_detail', 'api_brief_template_detail',
                             'api_question_detail','client_work_detail','client_money_detail']:
                url = self.live_server_url + reverse(view_name, args=[0])

            # add double <pk>-requiring views here:
            elif view_name in ['edit_service', 'service_detail']:
                url = self.live_server_url + reverse(view_name, args=[0,0])

            else:
                url = self.live_server_url + reverse(view_name)

            self.browser.get(url)

            try:
                h1 = self.browser.find_element_by_tag_name('h2')
            except NoSuchElementException:
                self.fail('h1 Element not found, page is not blocked: %s' % url)

            self.assertIn('Sign In', h1.text, 'Text not found on page: %s' % url)
            self.assertTrue(self.live_server_url + reverse('account_login') in self.browser.current_url)

    def test_can_access_contact(self):
        self.browser.get(self.live_server_url + reverse('contact'))

        self.assertIsNotNone(self.browser.find_element_by_class_name('sub-main'))

    def test_can_request_signup(self):
        b = self.browser
        b.get(self.live_server_url + reverse('signup'))
        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_name('company').send_keys('PPPPPPP')
        b.find_element_by_name('email').send_keys('PPPP@PPP.com')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Request sent.' in success_message.text)

    def test_feedback(self):
        b = self.browser
        b.get(self.live_server_url + reverse('feedback'))

        b.find_element_by_name('email').send_keys('foo@bar.com')
        b.find_element_by_name('feedback').send_keys('asdfasdfasdsadf')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertEqual(b.find_element_by_tag_name('body').text, 'Thank you.')