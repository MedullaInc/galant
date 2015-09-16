from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDown():
    browser.close()


class GallantServiceTest(browser.SignedInTest):
    def test_add_service(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_service'))

        b.find_element_by_name('name').send_keys('Branding')
        b.find_element_by_name('description').send_keys('asadasdfsd asd fasdf')
        b.find_element_by_name('cost_0').clear()
        b.find_element_by_name('cost_0').send_keys('10')
        b.find_element_by_name('quantity').send_keys('10')
        b.find_element_by_xpath('//select[@name="type"]/option[@value="0"]').click()
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Service saved.' in success_message.text)

    def test_edit_service(self):
        b = browser.instance()
        s = autofixture.create_one('gallant.Service', generate_fk=True,
                                   field_values={'user': self.user})
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

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Service saved.' in success_message.text)

    def test_add_service_note(self):
        b = browser.instance()
        s = autofixture.create_one('gallant.Service', generate_fk=True,
                                   field_values={'user': self.user})
        s.save()
        b.get(self.live_server_url + reverse('service_detail', args=[s.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="note.text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)