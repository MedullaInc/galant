from django.core.urlresolvers import reverse
import autofixture
from django.template import Context, Template
from functional_tests import browser
from rest_framework.test import APIRequestFactory
from selenium.common.exceptions import NoSuchElementException


def tearDownModule():
    browser.close()


class GallantClientTest(browser.SignedInTest):
    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_can_access_clients(self):
        # check 'Clients' h1
        self.get(self.live_server_url + reverse('clients'))

        app_title = self.e_class('app_title')
        self.assertEqual('Clients', app_title.text)

    def test_can_access_client_work(self):
        # Create client
        client = self.create_one('gallant.Client')

        # Create quote & services
        quote = self.create_one('quotes.Quote', {'client': client, 'status': '5'})
        services = autofixture.create('gallant.Service', 10, field_values={'user': self.user})

        # Assign services to quote
        for s in services[0:9]:
            quote.services.add(s)

        quote.save()

        # Create project
        project = self.create_one('gallant.Project', {'status': '2', 'quote': quote,
                                                      'services': [], 'client': None})

        # Add quote to project
        quote.projects.add(project)

        # Check 'Client Work' h1
        self.get(self.live_server_url + reverse('client_work_detail', args=[client.id]))

        app_title = self.e_class('app_title')
        self.assertEqual('Client Work', app_title.text)

        # Validate templatetags javascript
        project_work_data = self.b.execute_script("return project_work_data_%s;" % project.id)
        self.assertTrue(len(project_work_data) > 0)

        for work_data in project_work_data:
            if work_data['label'] == 'On Hold':
                self.assertTrue(work_data['value'] == 0)
            elif work_data['label'] == 'Unassigned':
                self.assertTrue(work_data['value'] == 9)
            elif work_data['label'] == 'Active':
                self.assertTrue(work_data['value'] == 0)
            elif work_data['label'] == 'Overdue':
                self.assertTrue(work_data['value'] == 0)
            elif work_data['label'] == 'Completed':
                self.assertTrue(work_data['value'] == 0)

        # Validate template Templatetags
        factory = APIRequestFactory()
        request = factory.patch(reverse('client_work_detail', args=[client.id]))
        request.user = self.user

        context = {'request': request, 'client': client, 'status': None}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% get_client_services_count request client status=None %}', context
        )

        self.assertEqual(rendered, u'9')

        context = {'request': request, 'client': client, 'status': 1}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% get_client_services_count request client status=1 %}', context
        )

        self.assertEqual(rendered, u'9')

        context = {'request': request, 'project': project, 'status': None}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% get_project_services request project status=None %}', context
        )

        self.assertNotEqual(rendered, u'[]')

        context = {'request': request, 'project': project, 'status': 1}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% get_project_services request project status=1 %}', context
        )

        self.assertGreater(len(rendered), 0)

        context = {'request': request, 'project': project, 'status': None}
        rendered = self.render_template(
            '{% load gallant_tags %}'
            '{% get_project_services_count request project status=None %}', context
        )

        self.assertEqual(rendered, u'9')

    def test_can_access_client_money(self):
        # check 'Client Money' h1
        c = self.create_one('gallant.Client')

        self.get(self.live_server_url + reverse('client_money_detail', args=[c.id]))

        app_title = self.e_class('app_title')
        self.assertEqual('Client Money', app_title.text)

    def test_add_client(self):
        self.get(self.live_server_url + reverse('add_client'))

        self.e_name('client.name').send_keys('Kanye West')
        self.e_name('client.email').send_keys('kanye@imaletyoufinish.com')
        self.click_xpath('//select[@name="client.status"]/option[@value="1"]')
        # self.e_xpath('//textarea[@name="notes"]').send_keys('asdf')

        # phone # field JS broken
        # self.e_name('contact_info.phone_number').send_keys('5281833666666')  # error here, digits are entered wrong
        self.e_name('contact_info.address').send_keys('asdf')
        self.e_name('contact_info.city').send_keys('asdf')
        self.e_name('contact_info.state').send_keys('asdf')
        self.e_name('contact_info.zip').send_keys('12345')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Client saved.' in success_message.text)

    def test_edit_client(self):
        c = self.create_one('gallant.Client')
        self.get(self.live_server_url + reverse('edit_client', args=[c.id]))

        self.e_name('client.name')
        self.e_name('client.name').send_keys('PPPPPPP')
        self.click_xpath('//select[@name="client.status"]/option[@value="3"]')
        # self.e_xpath('//textarea[@name="notes"]').send_keys('dddd')

        self.e_name('contact_info.phone_number').clear()
        # phone number JS broken for tests
        # self.e_name('contact_info.phone_number').send_keys('+52(81)8336-6666')
        self.e_name('contact_info.zip').clear()
        self.e_name('contact_info.zip').send_keys('12345')

        self.submit_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Client saved.' in success_message.text)

    def test_add_client_note(self):
        c = self.create_one('gallant.Client')
        self.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        test_string = '2351tlgkjqlwekjalfkj'
        self.e_class('fs-mini')

        self.e_xpath('//textarea[@name="note.text"]').send_keys(test_string)

        self.submit('note_add')

        notes = self.e_id('notes')

        self.assertTrue(test_string in notes.text)

    def test_client_soft_delete(self):

        # Create Client
        c = self.create_one('gallant.Client')

        # Access delete url
        self.get(self.live_server_url + reverse('delete_client', args=[c.id]))

        # Validate client detail returns 404
        response = self.client.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        self.assertEqual(response.status_code, 404)

    def test_blank_note_fail(self):
        c = self.create_one('gallant.Client')
        self.get(self.live_server_url + reverse('client_detail', args=[c.id]))
        self.click_xpath('//button[@type="submit"]')

        self.assertTrue('This field is required.' in self.e_class('help-block').text)

    def test_client_perms(self):
        c = self.create_one('gallant.Client')

        c2 = autofixture.create_one('gallant.Client', generate_fk=True)

        self.get(self.live_server_url + reverse('client_detail', args=[c.id]))

        app_title = self.e_class('app_title')
        self.assertEqual('Client - Dashboard', app_title.text)

        self.get(self.live_server_url + reverse('client_detail', args=[c2.id]))

        self.assertRaises(NoSuchElementException, self.b.find_element_by_class_name, 'app_title')

    def test_can_access_client_endpoint(self):
        s = self.create_one('gallant.Client')

        response = self.client.get(self.live_server_url + reverse('api_client_detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)
