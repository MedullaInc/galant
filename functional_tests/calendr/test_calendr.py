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
        self.get(self.live_server_url + reverse('calendr'))
        self.e_id('id_date')
        self.e_id('id_date').send_keys('11.09.2015')

        date = self.e_css('.fc-toolbar h2')
        self.assertIn(u'November 2015', date.text)

    def test_can_edit_task(self):
        self.get(self.live_server_url + reverse('calendr'))

        self.e_css('.fc-event')
        self.e_css('.fc-event').click()

        submit_task = self.e_id('submit_task')
        self.assertTrue(submit_task)

    def test_can_edit_project(self):
        s = self.create_one('calendr.Task')

        response = self.client.get(self.live_server_url + reverse('api-task-detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_change_view(self):
        self.get(self.live_server_url + reverse('calendr'))
        self.e_xpath('//tr[@data-resource-id="1"]')
        self.e_id('timelineWeek').click()

        self.assertTrue(self.e_css('.fc-timelineWeek-view'))

    @skip("TODO")
    def test_can_filter_task(self):
        self.get(self.live_server_url + reverse('calendr'))
        self.e_id('filterTask').click()
        self.assertTrue(self.e_id('searchText'))
