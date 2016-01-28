from datetime import timedelta

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.timezone import activate
from functional_tests import browser
import autofixture


def tearDown():
    browser.close()


def teardown_module(module):
    browser.close()


class CalendrTest(browser.SignedInTest):
    def setUp(self):
        super(CalendrTest, self).setUp()
        start = timezone.now() - timedelta(hours=+8)  # hack to account for browser timezone

        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})
        t = autofixture.create_one('calendr.Task',
                                   field_values={'user':self.user,'project':p,'daily_estimate':0.0, 'assignee':self.user, 'start':start, 'end':start})

        self.browser = browser.instance()
        self.disable_popups()

    def test_can_access_calendr(self):
        response = self.client.get(self.live_server_url + reverse('calendr'))
        self.assertEqual(response.status_code, 200)

    def test_can_access_task_endpoint(self):
        s = autofixture.create_one('calendr.Task', generate_fk=True,
                                   field_values={'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api-task-detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_change_date(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))
        browser.wait().until(lambda driver: driver.find_element_by_id('id_date'))
        b.find_element_by_id('id_date').send_keys('2015-11-09')

        date = b.find_element_by_css_selector('.fc-toolbar h2')
        self.assertTrue(u'November 2015' in date.text)

    def test_can_edit_task(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))

        browser.wait().until(lambda driver: driver.find_element_by_css_selector('.fc-event'))
        b.find_element_by_css_selector('.fc-event').click()

        submit_task = b.find_element_by_css_selector('#submitTask')
        self.assertTrue(submit_task)
    
    def test_can_edit_project(self):
        s = autofixture.create_one('calendr.Task', generate_fk=True,
                                   field_values={'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api-task-detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_change_view(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))
        browser.wait().until(lambda driver: driver.find_element_by_id('timelineWeek'))
        b.find_element_by_id('timelineWeek').click()

        timeline_view = b.find_element_by_class_name('fc-timelineWeek-view')
        self.assertTrue(timeline_view)

    def test_can_filter_task(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))
        browser.wait().until(lambda driver: driver.find_element_by_id('filterTask'))
        b.find_element_by_id('filterTask').click()

        search_task = b.find_element_by_id('searchText')
        self.assertTrue(search_task)
