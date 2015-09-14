from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser
from selenium.common.exceptions import NoSuchElementException


def tearDown():
    browser.close()


class GallantClientTest(browser.SignedInTest):
    def test_can_access_clients(self):
        # check 'Clients' h1
        browser.instance().get(self.live_server_url + reverse('clients'))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Clients', app_title.text)

    def test_add_client(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_client'))
        self.load_scripts()

        b.find_element_by_name('client.name').send_keys('Kanye West')
        b.find_element_by_name('client.email').send_keys('kanye@imaletyoufinish.com')
        b.find_element_by_xpath('//select[@name="client.type"]/option[@value="0"]').click()
        b.find_element_by_xpath('//select[@name="client.size"]/option[@value="0"]').click()
        b.find_element_by_xpath('//select[@name="client.status"]/option[@value="0"]').click()
        # b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        # phone # field JS broken
        # b.find_element_by_name('contact_info.phone_number').send_keys('5281833666666')  # error here, digits are entered wrong
        b.find_element_by_name('contact_info.address').send_keys('asdf')
        b.find_element_by_name('contact_info.city').send_keys('asdf')
        b.find_element_by_name('contact_info.state').send_keys('asdf')
        b.find_element_by_name('contact_info.zip').send_keys('12345')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Client saved.' in success_message.text)

    def test_edit_client(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()
        b.get(self.live_server_url + reverse('edit_client', args=[c.id]))
        self.load_scripts()

        b.find_element_by_name('client.name').send_keys('PPPPPPP')
        b.find_element_by_xpath('//select[@name="client.type"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="client.size"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="client.status"]/option[@value="3"]').click()
        # b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('dddd')

        b.find_element_by_name('contact_info.phone_number').clear()
        # phone number JS broken for tests
        # b.find_element_by_name('contact_info.phone_number').send_keys('+52(81)8336-6666')
        b.find_element_by_name('contact_info.zip').clear()
        b.find_element_by_name('contact_info.zip').send_keys('12345')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Client saved.' in success_message.text)

    def test_add_client_note(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)

    def test_blank_note_fail(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue('This field is required.' in b.find_element_by_id('notes').text)

    def test_client_perms(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})

        c2 = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))

        app_title = b.find_element_by_class_name('app_title')
        self.assertEqual('Client', app_title.text)

        b.get(self.live_server_url + reverse('client_detail', args=[c2.id]))

        self.assertRaises(NoSuchElementException, b.find_element_by_class_name, 'app_title')


