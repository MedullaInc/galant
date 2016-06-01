from django.contrib.auth import hashers
from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes.models.quote import QuoteStatus
from gallant import models as g


def tearDownModule():
    browser.close()


class QuotesSignedOutTest(browser.BrowserTest):
    def setUp(self):
        super(QuotesSignedOutTest, self).setUp()
        self.user = self.create_one('gallant.GallantUser', {'password': hashers.make_password('password')})
        c = self.create_one('gallant.Client', {'user': self.user})
        q = self.create_one('quotes.Quote', {'sections': [], 'services': [], 'language': 'en',
                                             'client': c, 'status': '1'})
        serv = g.Service.objects.create(user=q.user, name='service1', quantity=1, description='desc', type=1, index=0)
        q.services.add(serv)

        self.get(self.live_server_url + reverse('quote_detail', args=[q.token.hex]))

        self.e_id('service_0')
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
