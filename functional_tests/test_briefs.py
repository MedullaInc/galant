from django.core.urlresolvers import reverse
from functional_tests import browser


def tearDown():
    browser.close()


class BriefsSignedInTest(browser.SignedInTest):
    def test_can_access_briefs(self):
        # check 'Briefs' h1
        browser.instance().get(self.live_server_url + reverse('briefs'))
        h1 = browser.instance().find_element_by_tag_name('h1')
        self.assertIn('Briefs', h1.text)
