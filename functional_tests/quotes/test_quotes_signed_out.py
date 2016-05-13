from django.contrib.auth import hashers
from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
import autofixture
from quotes.models.quote import QuoteStatus


def tearDownModule():
    browser.close()


class QuotesSignedOutTest(browser.BrowserTest):
    def setUp(self):
        super(QuotesSignedOutTest, self).setUp()
        self.user = self.create_one('gallant.GallantUser', {'password': hashers.make_password('password')})
        c = self.create_one('gallant.Client', {'user': self.user})
        q = self.create_one('quotes.Quote', {'sections': [], 'services': [], 'language': 'en',
                                             'client': c, 'status': '1'})
        i = qm.Section.objects.create(user=q.user, name='intro', title='intro', text='intro text', index=0)
        m = qm.Section.objects.create(user=q.user, name='important_notes', title='notes', text='notes text', index=1)
        q.sections.add(i)
        q.sections.add(m)

        self.get(self.live_server_url + reverse('quote_detail', args=[q.token.hex]))

        self.e_id('section_0')
        self.q = q
        self.disable_popups()

    def test_can_access_quotes_token(self):
        self.assertEqual('Name: %s' % self.q.name, self.e_xpath('//*[@e-id="quote_name"]').text)

    def test_can_accept_quote(self):
        self.submit('quote_accept')
        self.q.refresh_from_db()
        self.assertEqual(int(self.q.status), QuoteStatus.Accepted.value)

    def test_can_reject_quote(self):
        self.submit('quote_reject')
        self.q.refresh_from_db()
        self.assertEqual(int(self.q.status), QuoteStatus.Rejected.value)
