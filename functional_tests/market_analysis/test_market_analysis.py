# coding=utf-8
from django.core.urlresolvers import reverse
from experiments.models import Experiment, ENABLED_STATE, Enrollment
from functional_tests import browser
from django.test.utils import override_settings


def tearDown():
    browser.close()


@override_settings(EXPERIMENTS_VERIFY_HUMAN=False)
class LandingPageTest(browser.BrowserTest):
    def setUp(self):
        super(LandingPageTest, self).setUp()
        self.browser = browser.instance()
        self.experiment = Experiment(name='waiting_list', state=ENABLED_STATE)
        self.experiment.save()

    def test_can_access_landing_pages(self):
        browser.instance().get(self.live_server_url + reverse('landing'))
        title = browser.instance().find_element_by_css_selector('h2 span.red_a')
        self.assertIn('Sign up for our waiting list', title.text)

    def test_can_access_workflow_experiment(self):
        browser.instance().delete_all_cookies()
        browser.instance().get(self.live_server_url + reverse('workflow_test'))
        title = browser.instance().find_element_by_css_selector('h1 span.red_a')
        self.assertIn(u'Do great creative work\nlike great agencies', title.text)

    def test_can_access_tool_experiment(self):
        browser.instance().delete_all_cookies()
        browser.instance().get(self.live_server_url + reverse('tool_test'))
        title = browser.instance().find_element_by_css_selector('h1 span.red_a')
        self.assertIn(u'Manage clients, send quotes,\ntrack projects \u2014 all in one place', title.text)

    def test_waiting_list_registration_error(self):
        b = self.browser

        browser.instance().get(self.live_server_url + reverse('landing'))

        # fill out form & save
        b.find_element_by_id('id_email').send_keys('bobafett@republicarmy.com')
        b.find_element_by_id('id_web').send_keys('www.republicarmy.com')

        b.find_element_by_id('submit_signup').click()

        name_error = b.find_element_by_css_selector('ul.errorlist li')

        self.assertTrue('Name is required.' in name_error.text)

    def test_waiting_list_registration(self):
        b = self.browser

        browser.instance().get(self.live_server_url + reverse('landing'))

        # fill out form & save
        b.find_element_by_id('id_name').send_keys('Boba Fett')
        b.find_element_by_id('id_email').send_keys('bobafett@republicarmy.com')
        b.find_element_by_id('id_web').send_keys('www.republicarmy.com')

        b.find_element_by_id('submit_signup').click()

        success_message = b.find_element_by_class_name('red_a')

        self.assertTrue('Thank you' in success_message.text)
