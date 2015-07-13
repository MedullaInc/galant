from django.test import LiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import django


class SignedInTest(LiveServerTestCase):
    fixtures = ['functional_tests/fixtures/ft_one_user_logged_in.json']
    cookie = {u'domain': u'localhost', u'name': u'sessionid', u'value': u'88f6ox013p6m2i99kv220svrk9y6y16n',
                u'path': u'/', u'httponly': True, u'secure': False}

    def setUp(self):
        self.browser = webdriver.PhantomJS()

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # add session cookie for logged-in user
        self.browser.add_cookie(self.cookie)

    def tearDown(self):
        self.browser.quit()

    def load_scripts(self):
        '''
        Call this method after loading target page to load jQuery and scripts contained
        within <body> (Selenium doesn't automatically load them).
        :return:
        '''
        b = self.browser
        with open("static/js/jquery-latest.min.js", "r") as jq:
            b.execute_script(jq.read())

        scripts = b.find_elements_by_xpath('//body/script')
        for s in scripts:
            b.execute_script(s.get_attribute('innerHTML'))

        # need this to auto-accept all confirmation dialogs
        b.execute_script("window.confirm = function(){return true;}")
        b.execute_script("window.alert = function(){}")


class LoginSignUpTest(SignedInTest):
    fixtures = ['functional_tests/fixtures/ft_one_user_logged_in.json']

    def setUp(self):
        super(LoginSignUpTest, self).setUp()
        self.browser.get(self.live_server_url)

    def test_cant_login(self):
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Account Login', body.text)

    def test_cant_sign_up(self):
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Sign Up Now!', body.text)

    def test_can_sign_out(self):
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Sign Out', body.text)


class GallantSignedInTest(SignedInTest):
    fixtures = ['functional_tests/fixtures/ft_one_user_logged_in.json',
                'functional_tests/fixtures/ft_client.json',
                'functional_tests/fixtures/ft_service.json']

    def test_add_client(self):
        b = self.browser
        b.get(self.live_server_url + reverse('add_client'))

        b.find_element_by_name('name').send_keys('Kanye West')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="0"]').click()
        b.find_element_by_xpath('//select[@name="size"]/option[@value="0"]').click()
        b.find_element_by_xpath('//select[@name="status"]/option[@value="0"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Client', h3.text)

    def test_edit_client(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_client', args=[1]))

        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="size"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="status"]/option[@value="3"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('dddd')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Client', h3.text)

    def test_add_client_note(self):
        b = self.browser
        b.get(self.live_server_url + reverse('client_detail', args=[1]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)

    def test_blank_note_fail(self):
        b = self.browser
        b.get(self.live_server_url + reverse('client_detail', args=[1]))
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue('This field is required.' in b.find_element_by_id('notes').text)

    def test_add_service(self):
        b = self.browser
        b.get(self.live_server_url + reverse('add_service'))

        b.find_element_by_name('name').send_keys('Branding')
        b.find_element_by_name('description').send_keys('asadasdfsd asd fasdf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('10')
        b.find_element_by_name('quantity').send_keys('10')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="0"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')

        self.assertEqual(u'Service', h3.text)

    def test_edit_service(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_service', args=[1]))

        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_name('description').send_keys('phpjpjpjpjpjpf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('99')
        b.find_element_by_name('quantity').send_keys('88')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="3"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys(';;;;;;;;;')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Service', h3.text)

    def test_add_service_note(self):
        b = self.browser
        b.get(self.live_server_url + reverse('service_detail', args=[1]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)