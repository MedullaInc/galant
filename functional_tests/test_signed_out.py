from django.test import LiveServerTestCase
from selenium import webdriver

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

    def test_can_login(self):
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Account Login', body.text)

    def test_can_sign_up(self):
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Sign Up Now!', body.text)

