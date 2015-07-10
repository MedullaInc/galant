from django.core.urlresolvers import reverse
from test_signed_in import SignedInTest


class QuotesSignedInTest(SignedInTest):
    fixtures = ['functional_tests/fixtures/ft_one_user.json',
                'functional_tests/fixtures/ft_client.json',
                'functional_tests/fixtures/ft_service.json',
                'functional_tests/fixtures/ft_quote.json']

    def test_can_access_quotes(self):
        # check 'Quotes' h1
        self.browser.get(self.live_server_url + reverse('quotes'))
        h1 = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Quotes', h1.text)

    def test_add_quote(self):
        b = self.browser
        b.get(self.live_server_url + reverse('add_quote'))

        b.find_element_by_name('name').send_keys('Quote test')
        b.find_element_by_xpath('//select[@name="client"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="intro"]/option[@value="1"]').click()
        b.find_element_by_xpath('//select[@name="language"]/option[@value="en"]').click()
        b.find_element_by_xpath('//select[@name="margin_section"]/option[@value="1"]').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        self.assertEqual(b.current_url, self.live_server_url + reverse('home'))

    def test_edit_quote(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_quote', args=[1]))

        b.find_element_by_name('name').send_keys('Quote test edit')
        b.find_element_by_xpath('//select[@name="client"]/option[@value="2"]').click()
        b.find_element_by_xpath('//select[@name="intro"]/option[@value="2"]').click()
        b.find_element_by_xpath('//select[@name="language"]/option[@value="en"]').click()
        b.find_element_by_xpath('//select[@name="margin_section"]/option[@value="2"]').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Quote', h3.text)
