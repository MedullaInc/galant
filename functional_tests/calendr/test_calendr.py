from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDown():
    browser.close()


class CalendrTest(browser.SignedInTest):
    def test_can_access_calendr(self):
        response = self.client.get(self.live_server_url + reverse('calendr'))
        self.assertEqual(response.status_code, 200)

    def test_can_access_service_endpoint(self):
        s = autofixture.create_one('gallant.Service', generate_fk=True,
                                   field_values={'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api_service_detail', args=[s.id]))
        self.assertEqual(response.status_code, 200)
