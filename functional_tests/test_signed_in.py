from django.test import LiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse

class SignedInTest(LiveServerTestCase):
    fixtures = ['functional_tests/fixtures/ft_one_user.json',
                'functional_tests/fixtures/ft_client.json',
                'functional_tests/fixtures/ft_service.json']

    def setUp(self):
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

    '''def test_can_access_briefs(self):
        # check 'Briefs' h1
        self.browser.get(self.live_server_url + reverse('briefs'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Briefs', h1.text)
    '''

    def test_can_access_quotes(self):
        # check 'Quotes' h1
        self.browser.get(self.live_server_url + reverse('quotes'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Quotes', h1.text)

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
