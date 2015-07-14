from django.core.urlresolvers import reverse
from functional_tests.test_signed_in import SignedInTest, get_browser, quit_browser


def teardown():
    quit_browser()


class BriefsSignedInTest(SignedInTest):
    def test_can_access_briefs(self):
        # check 'Briefs' h1
        get_browser().get(self.live_server_url + reverse('briefs'))
        h1 = get_browser().find_element_by_tag_name('h1')
        self.assertIn('Briefs', h1.text)
