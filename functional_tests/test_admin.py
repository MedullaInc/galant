from django.test import LiveServerTestCase
from selenium import webdriver

class AdminTest(LiveServerTestCase):
    fixtures = ['functional_tests/fixtures/ft_admin.json']

    def setUp(self):
        self.browser = webdriver.PhantomJS()

        # other browsers can be set here, eg
        #self.browser = webdriver.Firefox()

        # open web browser, go to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        email_field = self.browser.find_element_by_name('username')
        password_field = self.browser.find_element_by_name('password')

        email_field.send_keys('test@test.com')
        password_field.send_keys('test2015')

        submit = self.browser.find_element_by_css_selector('form input[value="Log in"]')
        submit.click()

    def tearDown(self):
        self.browser.quit()

    def test_can_access_admin_site(self):
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

