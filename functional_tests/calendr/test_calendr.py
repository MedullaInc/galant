from django.core.urlresolvers import reverse
from functional_tests import browser


def tearDown():
    browser.close()


class CalendrTest(browser.SignedInTest):
    def test_can_access_calendr(self):
        browser.instance().get(self.live_server_url + reverse('calendr'))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Calendar', app_title.text)
        