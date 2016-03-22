from django.contrib.auth import hashers
from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
import autofixture
from quotes.models.quote import QuoteStatus


def tearDownModule():
    browser.close()


def get_blank_quote_autofixture(user):
    c = autofixture.create_one('gallant.Client', generate_fk=True,
                               field_values={'user': user})
    q = autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'sections': [],'services': [], 'language': 'en',
                                             'user': user, 'client': c, 'status': '1'})
    i = qm.Section.objects.create(user=q.user, name='intro', title='intro', text='intro text', index=0)
    m = qm.Section.objects.create(user=q.user, name='important_notes', title='notes', text='notes text', index=1)
    q.sections.add(i)
    q.sections.add(m)
    return q


class QuotesSignedInTest(browser.BrowserTest):
    def setUp(self):
        super(browser.BrowserTest, self).setUp()
        self.user = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                           field_values={'password': hashers.make_password('password')})
        self.disable_popups()

    def test_can_access_quotes_token(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.token.hex]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        self.assertEqual('Name: %s' % q.name, b.find_element_by_xpath('//*[@e-id="quote_name"]').text)

    def test_can_accept_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.token.hex]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        with browser.wait_for_page_load():
            b.find_element_by_id('quote_accept').click()
        q.refresh_from_db()
        self.assertEqual(int(q.status), QuoteStatus.Accepted.value)

    def test_can_reject_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.token.hex]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        with browser.wait_for_page_load():
            b.find_element_by_id('quote_reject').click()
        q.refresh_from_db()
        self.assertEqual(int(q.status), QuoteStatus.Rejected.value)
