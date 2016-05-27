from django.core.urlresolvers import reverse
from functional_tests import browser
from gallant.enums import ProjectStatus, ClientStatus


def tearDownModule():
    browser.close()


class GallantProjectTest(browser.SignedInTest):
    def test_add_project(self):
        q = self.create_one('quotes.Quote')
        self.get(self.live_server_url + reverse('add_project', args=[q.id]))

        self.e_name('name').send_keys('Branding')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

    def test_edit_project(self):

        # Add Project
        c = self.create_one('gallant.Client')
        q = self.create_one('quotes.Quote', {'client': c, 'status': 5})

        self.get(self.live_server_url + reverse('add_project', args=[q.id]))

        self.e_name('name').send_keys('Branding')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

        self.create_one('quotes.Quote', {'name': "XXX", 'client': c, 'status': 5})

        # Edit Project removing one quote
        self.click_id('edit_project')

        self.click_id('id_linked_quotes_0')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

        # Edit Project with extra quote
        self.click_id('edit_project')

        self.e_name('name').send_keys('PPPPPPP')

        self.click_id('id_available_quotes_0')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Project saved.' in success_message.text)

    def test_add_project_note(self):
        p = self.create_one('gallant.Project')
        self.create_one('quotes.Quote', {'project': p})
        c = p.quote_set.all_for(p.user)[0].client;
        c.auto_pipeline = True
        c.status = ClientStatus.Project_Underway.value
        c.save()

        p.status = ProjectStatus.Overdue.value
        p.save()

        self.get(self.live_server_url + reverse('project_detail', args=[p.id]))
        test_string = '2351tlgkjqlwekjalfkj'

        self.e_xpath('//textarea[@name="note.text"]').send_keys(test_string)
        self.submit_xpath('//button[@type="submit"]')

        self.assertTrue(test_string in self.e_id('notes').text)

    def test_project_soft_delete(self):

        # Create Project
        p = self.create_one('gallant.Project')

        # Access delete url
        self.get(self.live_server_url + reverse('delete_project', args=[p.id]))

        # Validate project detail returns 404
        response = self.client.get(self.live_server_url + reverse('project_detail', args=[p.id]))
        self.assertEqual(response.status_code, 404)

    def test_can_access_project_endpoint(self):
        s = self.create_one('gallant.Project')

        response = self.client.get(self.live_server_url + reverse('api_project_detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)
