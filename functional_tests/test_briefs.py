from django.core.urlresolvers import reverse
from test_signed_in import SignedInTest


class BriefsSignedInTest(SignedInTest):
    def test_can_access_briefs(self):
        # check 'Briefs' h1
        self.browser.get(self.live_server_url + reverse('briefs'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Briefs', h1.text)
