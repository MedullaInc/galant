from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDownModule():
    browser.close()


class GallantServiceTest(browser.SignedInTest):
    def test_add_service(self):
        b = browser.instance()

        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})

        autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'user': self.user, 'project': p})

        b.get(self.live_server_url + reverse('add_service', args=[p.id]))

        b.find_element_by_name('name').send_keys('Branding')
        b.find_element_by_name('description').send_keys('asadasdfsd asd fasdf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('10')
        b.find_element_by_name('quantity').send_keys('10')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="0"]').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Service saved.' in success_message.text)

    def test_edit_service(self):
        b = browser.instance()
        s = autofixture.create_one('gallant.Service', generate_fk=True,
                                   field_values={'user': self.user})
        s.save()

        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})

        autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'user': self.user, 'project': p})

        b.get(self.live_server_url + reverse('edit_service', args=[p.id, s.id]))

        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_name('description').send_keys('phpjpjpjpjpjpf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('99')
        b.find_element_by_name('quantity').send_keys('88')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="3"]').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Service saved.' in success_message.text)

    def test_add_service_note(self):
        b = browser.instance()
        s = autofixture.create_one('gallant.Service', generate_fk=True,
                                   field_values={'user': self.user})
        s.save()

        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})

        autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'user': self.user, 'project': p})

        b.get(self.live_server_url + reverse('service_detail', args=[p.id, s.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="note.text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()
        
        s.refresh_from_db()
        self.assertEqual(s.notes.count(), 1)

        self.assertTrue(test_string in b.find_element_by_id('notes').text)

    def test_can_access_service_endpoint(self):
        s = autofixture.create_one('gallant.Service', generate_fk=True,
                                   field_values={'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api_service_detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)