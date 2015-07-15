from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDown():
    browser.close()


class GallantClientTest(browser.SignedInTest):
    def test_can_access_clients(self):
        # check 'Clients' h1
        browser.get().get(self.live_server_url + reverse('clients'))
        h1 = browser.get().find_element_by_tag_name('h1')
        self.assertIn('Clients', h1.text)

    def test_add_client(self):
        b = browser.instance()
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
        b = browser.instance()
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
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)

    def test_blank_note_fail(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue('This field is required.' in b.find_element_by_id('notes').text)
