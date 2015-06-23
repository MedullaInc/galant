from django.test import LiveServerTestCase
from selenium import webdriver
from django.utils.translation import activate
from django.core.urlresolvers import reverse

class SignedInTest(LiveServerTestCase):
    fixtures = ['functional_tests/fixtures/ft_one_user.json']

    def setUp(self):
        activate('en')
        self.browser = webdriver.PhantomJS()

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # open web browser, go to the admin page
        self.browser.get(self.live_server_url)

        email_field = self.browser.find_element_by_name('login')
        password_field = self.browser.find_element_by_name('password')

        email_field.send_keys('david.agg@gmail.com')
        password_field.send_keys('asdfasdf')

        submit = self.browser.find_element_by_name('submit_login')
        submit.click()

    def tearDown(self):
        self.browser.quit()

    def test_can_login(self):
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Account Login', body.text)

    def test_can_sign_up(self):
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Sign Up Now!', body.text)

    def test_can_sign_out(self):
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Sign Out', body.text)

    def test_can_access_briefs(self):
        # check 'Briefs' h1
        self.browser.get(self.live_server_url + reverse('briefs'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Briefs', h1.text)
