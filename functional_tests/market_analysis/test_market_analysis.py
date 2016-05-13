# coding=utf-8
from django.core.urlresolvers import reverse
from experiments.models import Experiment, ENABLED_STATE, Enrollment
from functional_tests import browser
from django.test.utils import override_settings


def tearDownModule():
    browser.close()


@override_settings(EXPERIMENTS_VERIFY_HUMAN=False)
class LandingPageTest(browser.BrowserTest):
    def setUp(self):
        super(LandingPageTest, self).setUp()
        self.experiment = Experiment(name='waiting_list', state=ENABLED_STATE)
        self.experiment.save()

    def test_can_access_landing_pages(self):
        self.get(self.live_server_url + reverse('landing'))
        title = self.e_css('h2 span.red_a')
        self.assertIn('Sign up for our waiting list', title.text)

    def test_can_access_workflow_experiment(self):
        self.b.delete_all_cookies()
        self.get(self.live_server_url + reverse('workflow_test'))
        title = self.e_css('h1 span.red_a')
        self.assertIn(u'Use the proven workflow\nfrom creative agencies worldwide', title.text)

    def test_can_access_tool_experiment(self):
        self.b.delete_all_cookies()
        self.get(self.live_server_url + reverse('tool_test'))
        title = self.e_css('h1 span.red_a')
        self.assertIn(u'Manage clients, send quotes,\ntrack projects \u2014 all in one place', title.text)

    def test_waiting_list_registration_error(self):
        self.get(self.live_server_url + reverse('landing'))

        # fill out form & save
        self.e_id('id_email').send_keys('bobafett@republicarmy.com')
        self.e_id('id_web').send_keys('www.republicarmy.com')

        self.click_id('submit_signup')

        name_error = self.e_css('ul.errorlist li')

        self.assertTrue('Name is required.' in name_error.text)

    def test_waiting_list_registration(self):
        self.get(self.live_server_url + reverse('landing'))

        # fill out form & save
        self.e_id('id_name').send_keys('Boba Fett')
        self.e_id('id_email').send_keys('bobafett@republicarmy.com')
        self.e_id('id_web').send_keys('www.republicarmy.com')

        self.click_id('submit_signup')

        success_message = self.e_class('red_a')

        self.assertTrue('Thank you' in success_message.text)
