from django.core.urlresolvers import reverse
from functional_tests import browser


def teardown():
    browser.quit()


class BriefsSignedInTest(browser.SignedInTest):
    def test_can_access_briefs(self):
        # check 'Briefs' h1
        browser.get().get(self.live_server_url + reverse('briefs'))
        h1 = browser.get().find_element_by_tag_name('h1')
        self.assertIn('Briefs', h1.text)
