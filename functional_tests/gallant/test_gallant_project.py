from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDown():
    browser.close()


class GallantProjectTest(browser.SignedInTest):
    def test_add_project(self):
        b = browser.instance()
        q = autofixture.create_one('quotes.Quote', generate_fk=True,
                                   field_values={'user': self.user})
        b.get(self.live_server_url + reverse('add_project', args=[q.id]))

        b.find_element_by_name('name').send_keys('Branding')
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys('asdf')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

    def test_edit_project(self):
        b = browser.instance()
        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})
        autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'user': self.user, 'project': p})
        b.get(self.live_server_url + reverse('edit_project', args=[p.id]))

        b.find_element_by_name('name').send_keys('PPPPPPP')
        b.find_element_by_xpath('//textarea[@name="notes"]').send_keys(';;;;;;;;;')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

    def test_add_project_note(self):
        b = browser.instance()
        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})
        autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'user': self.user, 'project': p})

        b.get(self.live_server_url + reverse('project_detail', args=[p.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        b.find_element_by_xpath('//textarea[@name="note.text"]').send_keys(test_string)
        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertTrue(test_string in b.find_element_by_id('notes').text)