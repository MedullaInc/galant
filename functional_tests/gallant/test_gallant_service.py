from django.core.urlresolvers import reverse
from functional_tests import browser


def tearDownModule():
    browser.close()


class GallantServiceTest(browser.SignedInTest):
    def test_add_service(self):
        p = self.create_one('gallant.Project')
        self.create_one('quotes.Quote', {'project': p})

        self.get(self.live_server_url + reverse('add_service', args=[p.id]))

        self.e_name('name').send_keys('Branding')
        self.e_name('description').send_keys('asadasdfsd asd fasdf')
        self.e_name('cost_0').clear()
        self.e_name('cost_0').send_keys('10')
        self.e_name('quantity').send_keys('10')
        self.click_xpath('//select[@name="type"]/option[@value="0"]')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Service saved.' in success_message.text)

    def test_edit_service(self):
        s = self.create_one('gallant.Service')
        p = self.create_one('gallant.Project')

        self.create_one('quotes.Quote', {'project': p})

        self.get(self.live_server_url + reverse('edit_service', args=[p.id, s.id]))

        self.e_name('name').send_keys('PPPPPPP')
        self.e_name('description').send_keys('phpjpjpjpjpjpf')
        self.e_name('cost_0').clear()
        self.e_name('cost_0').send_keys('99')
        self.e_name('quantity').send_keys('88')
        self.click_xpath('//select[@name="type"]/option[@value="3"]')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Service saved.' in success_message.text)

    def test_add_service_note(self):
        s = self.create_one('gallant.Service')

        p = self.create_one('gallant.Project')

        self.create_one('quotes.Quote', {'project': p})

        self.get(self.live_server_url + reverse('service_detail', args=[p.id, s.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        self.e_xpath('//textarea[@name="note.text"]').send_keys(test_string)

        self.submit_xpath('//button[@type="submit"]')
        
        s.refresh_from_db()
        self.assertEqual(s.notes.count(), 1)

        self.assertTrue(test_string in self.e_id('notes').text)

    def test_can_access_service_endpoint(self):
        s = self.create_one('gallant.Service')

        response = self.client.get(self.live_server_url + reverse('api_service_detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)