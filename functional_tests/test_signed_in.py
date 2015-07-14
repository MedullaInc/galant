from django.test import LiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import autofixture
from django.contrib.auth import hashers


browser = []


def get_browser():
    if len(browser) < 1:
        browser.append(webdriver.PhantomJS())
    return browser[0]


def quit_browser():
    get_browser().quit()
    browser.pop(0)


def teardown():
    quit_browser()


class SignedInTest(LiveServerTestCase):
    def setUp(self):
        u = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                   field_values={'password': hashers.make_password('password')})
        u.save()

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # add session cookie for logged-in user
        self.client.login(email=u.email, password='password')
        get_browser().add_cookie({u'domain': u'localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

    def load_scripts(self):
        '''
        Call this method after loading target page to load jQuery and scripts contained
        within <body> (Selenium doesn't automatically load them).
        :return:
        '''
        b = get_browser()
        with open("static/js/jquery-latest.min.js", "r") as jq:
            b.execute_script(jq.read())

        scripts = b.find_elements_by_xpath('//body/script')
        for s in scripts:
            b.execute_script(s.get_attribute('innerHTML'))

        # need this to auto-accept all confirmation dialogs
        b.execute_script("window.confirm = function(){return true;}")
        b.execute_script("window.alert = function(){}")


class LoginSignUpTest(SignedInTest):
    def setUp(self):
        super(LoginSignUpTest, self).setUp()
        get_browser().get(self.live_server_url)

    def test_cant_login(self):
        body = get_browser().find_element_by_tag_name('body')
        self.assertNotIn('Account Login', body.text)

    def test_cant_sign_up(self):
        body = get_browser().find_element_by_tag_name('body')
        self.assertNotIn('Sign Up Now!', body.text)

    def test_can_sign_out(self):
        body = get_browser().find_element_by_tag_name('body')
        self.assertIn('Sign Out', body.text)


class GallantSignedInTest(SignedInTest):
    def test_add_client(self):
        b = get_browser()
        b.get(self.live_server_url + reverse('add_client'))

        b.find_element_by_name('name').send_keys('Kanye West')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="0"]').click()
        b.find_element_by_xpath('//select[@name="size"]/option[@value="0"]').click()
        b.find_element_by_xpath('//select[@name="status"]/option[@value="0"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = b.find_element_by_tag_name('h3')
        self.assertEqual(u'Client', h3.text)

    def test_edit_client(self):
        b = get_browser()
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('edit_client', args=[c.id]))

        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="size"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="status"]/option[@value="3"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('dddd')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = b.find_element_by_tag_name('h3')
        self.assertEqual(u'Client', h3.text)

    def test_add_client_note(self):
        b = get_browser()
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)

    def test_blank_note_fail(self):
        b = get_browser()
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue('This field is required.' in b.find_element_by_id('notes').text)

    def test_add_service(self):
        b = get_browser()
        b.get(self.live_server_url + reverse('add_service'))

        b.find_element_by_name('name').send_keys('Branding')
        b.find_element_by_name('description').send_keys('asadasdfsd asd fasdf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('10')
        b.find_element_by_name('quantity').send_keys('10')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="0"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = b.find_element_by_tag_name('h3')

        self.assertEqual(u'Service', h3.text)

    def test_edit_service(self):
        b = get_browser()
        s = autofixture.create_one('gallant.Service', generate_fk=True)
        s.save()
        b.get(self.live_server_url + reverse('edit_service', args=[s.id]))

        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_name('description').send_keys('phpjpjpjpjpjpf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('99')
        b.find_element_by_name('quantity').send_keys('88')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="3"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys(';;;;;;;;;')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = b.find_element_by_tag_name('h3')
        self.assertEqual(u'Service', h3.text)

    def test_add_service_note(self):
        b = get_browser()
        s = autofixture.create_one('gallant.Service', generate_fk=True)
        s.save()
        b.get(self.live_server_url + reverse('service_detail', args=[s.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)