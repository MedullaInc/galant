from django.core.urlresolvers import reverse
from functional_tests import browser


def tearDown():
    browser.close()


class CalendrTest(browser.SignedInTest):
    def test_can_access_calendr(self):
        response = self.client.get(self.live_server_url + reverse('calendr'))
        self.assertEqual(response.status_code, 200)