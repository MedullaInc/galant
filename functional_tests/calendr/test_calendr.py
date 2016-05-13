from datetime import timedelta
from unittest.case import skip

from django.core.urlresolvers import reverse
from django.utils import timezone
from functional_tests import browser


def tearDownModule():
    browser.close()


class CalendrTest(browser.SignedInTest):
    def setUp(self):
        super(CalendrTest, self).setUp()
        start = timezone.now() - timedelta(hours=+8)  # hack to account for browser timezone

        p = self.create_one('gallant.Project')
        t = self.create_one('calendr.Task', {'project': p, 'daily_estimate': 0.0,
                                             'assignee': self.user, 'start': start, 'end': start})

        self.browser = browser.instance()
        self.disable_popups()

    def test_can_access_calendr(self):
        response = self.client.get(self.live_server_url + reverse('calendr'))
        self.assertEqual(response.status_code, 200)

    def test_can_access_task_endpoint(self):
        s = self.create_one('calendr.Task')

        response = self.client.get(self.live_server_url + reverse('api-task-detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_change_date(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))
        browser.wait().until(lambda driver: driver.find_element_by_id('id_date'))
        b.find_element_by_id('id_date').send_keys('11.09.2015')

        date = b.find_element_by_css_selector('.fc-toolbar h2')
        self.assertIn(u'November 2015', date.text)

    def test_can_edit_task(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))

        browser.wait().until(lambda driver: driver.find_element_by_css_selector('.fc-event'))
        b.find_element_by_css_selector('.fc-event').click()

        submit_task = b.find_element_by_css_selector('#submit_task')
        self.assertTrue(submit_task)

    def test_can_edit_project(self):
        s = self.create_one('calendr.Task')

        response = self.client.get(self.live_server_url + reverse('api-task-detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_change_view(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//tr[@data-resource-id="1"]'))
        browser.wait().until(lambda driver: driver.find_element_by_id('timelineWeek')).click()

        self.assertTrue(browser.wait().until(lambda driver: driver.find_element_by_css_selector('.fc-timelineWeek-view')))

    @skip("TODO")
    def test_can_filter_task(self):
        b = self.browser

        b.get(self.live_server_url + reverse('calendr'))
        browser.wait().until(lambda driver: driver.find_element_by_id('filterTask'))
        b.find_element_by_id('filterTask').click()
        browser.wait().until(lambda driver: driver.find_element_by_id('searchText'))
        search_task = b.find_element_by_id('searchText')
        self.assertTrue(search_task)
