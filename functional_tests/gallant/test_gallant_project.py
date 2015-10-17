from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDown():
    browser.close()


class GallantProjectTest(browser.SignedInTest):
    def test_project_list(self):
        b = browser.instance()
        q = autofixture.create_one('quotes.Quote', generate_fk=True,
                                   field_values={'user': self.user})
        b.get(self.live_server_url + reverse('add_project', args=[q.id]))

        b.find_element_by_name('name').send_keys('Branding')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        b.get(self.live_server_url + reverse('projects'))
        success_message = b.find_element_by_class_name('app_title')
        self.assertTrue(u'Projects' in success_message.text)

    def test_add_project(self):
        b = browser.instance()
        q = autofixture.create_one('quotes.Quote', generate_fk=True,
                                   field_values={'user': self.user})
        b.get(self.live_server_url + reverse('add_project', args=[q.id]))

        b.find_element_by_name('name').send_keys('Branding')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

    def test_edit_project(self):
        b = browser.instance()

        # Add Project
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        q = autofixture.create_one('quotes.Quote', generate_fk=True,
                                   field_values={'user': self.user, 'client': c, 'status': 5})

        b.get(self.live_server_url + reverse('add_project', args=[q.id]))

        b.find_element_by_name('name').send_keys('Branding')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

        autofixture.create_one('quotes.Quote', generate_fk=False,
                               field_values={'name': "XXX", 'user': self.user, 'client': c, 'status': 5})

        # Edit Project removing one quote
        b.find_element_by_id('edit_project').click()

        b.find_element_by_id('id_linked_quotes_0').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

        # Edit Project with extra quote
        b.find_element_by_id('edit_project').click()

        b.find_element_by_name('name').send_keys('PPPPPPP')

        b.find_element_by_id('id_available_quotes_0').click()

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

    def test_project_soft_delete(self):
        b = browser.instance()

        # Create Project
        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})

        # Access delete url
        b.get(self.live_server_url + reverse('delete_project', args=[p.id]))

        # Validate project detail returns 404
        response = self.client.get(self.live_server_url + reverse('project_detail', args=[p.id]))
        self.assertEqual(response.status_code, 404)

    def test_can_access_project_endpoint(self):
        s = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api_project_detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)
