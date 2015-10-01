import time
from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
import autofixture


def tearDown():
    browser.close()


def get_blank_quote_autofixture(user):
    c = autofixture.create_one('gallant.Client', generate_fk=True,
                               field_values={'user': user})
    q = autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'sections': [], 'language': 'en',
                                             'user': user, 'client': c})
    i = qm.TextSection.objects.create(user=q.user, name='intro', index=0)
    m = qm.TextSection.objects.create(user=q.user, name='important_notes', index=1)
    q.sections.add(i)
    q.sections.add(m)
    return q


class QuotesSignedInTest(browser.SignedInTest):
    def test_can_access_quotes(self):
        # check 'Quotes' h1
        browser.instance().get(self.live_server_url + reverse('quotes'))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Quotes', app_title.text)

    def test_access_quote_preview(self):
        q = get_blank_quote_autofixture(self.user)
        browser.instance().get(self.live_server_url + reverse('quote_preview', args=[q.id]))

        page_wrapper = browser.instance().find_element_by_class_name('page-wrapper')
        self.assertTrue(page_wrapper)

    def test_access_quote_header(self):
        q = get_blank_quote_autofixture(self.user)
        browser.instance().get(self.live_server_url + reverse('quote_header', args=[q.id]))

        header = browser.instance().find_element_by_class_name('header')
        self.assertTrue(header)

    def test_access_quote_footer(self):
        q = get_blank_quote_autofixture(self.user)
        browser.instance().get(self.live_server_url + reverse('quote_footer', args=[q.id]))

        footer = browser.instance().find_element_by_class_name('footer')
        self.assertTrue(footer)

    def test_add_quote(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()
        b.get(self.live_server_url + reverse('add_quote'))

        b.find_element_by_name('name').send_keys('Quote test')
        b.find_element_by_xpath('//select[@name="client"]/option[@value="%d"]' % c.id).click()
        b.find_element_by_id('id_-section-0-title').send_keys('test intro title')
        b.find_element_by_id('id_-section-0-text').send_keys('test intro text')
        b.find_element_by_id('id_-section-1-title').send_keys('test important notes title')
        b.find_element_by_id('id_-section-1-text').send_keys('test important notes text')
        b.find_element_by_xpath('//select[@name="-service-2-type"]/option[@value="3"]').click()

        self._submit_and_check(b)

    def test_edit_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))

        b.find_element_by_id('id_-section-0-title').clear()
        b.find_element_by_id('id_-section-0-title').send_keys('modified intro title')

        self._submit_and_check(b)

        intro = b.find_element_by_xpath('//div[@id="intro"]//h2')
        self.assertEqual(intro.text, 'modified intro title')

    def test_delete_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('delete_quote', args=[q.id]))

        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[q.id]))
        self.assertEqual(response.status_code, 404)

    def test_add_sections(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()

        b.find_element_by_id('id_-section-2-title').send_keys('1234')
        b.find_element_by_id('id_-section-2-text').send_keys('1234')
        b.find_element_by_id('id_-section-3-title').send_keys('4321')
        b.find_element_by_id('id_-section-3-text').send_keys('4321')

        self._submit_and_check(b)

        intro = b.find_element_by_xpath('//div[@id="section_1"]//h2')
        self.assertEqual(intro.text, '1234')

        intro = b.find_element_by_xpath('//div[@id="section_2"]//h2')
        self.assertEqual(intro.text, '4321')

    def test_add_service(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))

        add_service = b.find_element_by_id('add_service')
        add_service.click()
        add_service.click()

        b.find_element_by_id('id_-service-2-name').send_keys('1234')
        b.find_element_by_xpath('//select[@name="-service-2-type"]/option[@value="3"]').click()
        b.find_element_by_id('id_-service-3-name').send_keys('1234')
        b.find_element_by_xpath('//select[@name="-service-3-type"]/option[@value="3"]').click()

        self._submit_and_check(b)

        name = b.find_element_by_class_name('service_name')
        self.assertEqual(name.text, '1234')

    def test_section_order(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_-section-2-title').send_keys('1234')
        b.find_element_by_id('id_-section-2-text').send_keys('1234')
        b.find_element_by_id('id_-section-3-title').send_keys('s2title')
        b.find_element_by_id('id_-section-3-text').send_keys('s2text')
        b.find_element_by_id('id_-section-4-title').send_keys('s3title')
        b.find_element_by_id('id_-section-4-text').send_keys('s3text')

        self._submit_and_check(b)

        el = b.find_element_by_xpath('//div[@id="section_1"]//h2')
        self.assertEqual(el.text, '1234')

        el = b.find_element_by_xpath('//div[@id="section_3"]//h2')
        self.assertEqual(el.text, 's3title')

    def test_remove_section(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.disable_popups()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_-section-2-title').send_keys('1234')
        b.find_element_by_id('id_-section-2-text').send_keys('1234')
        b.find_element_by_id('id_-section-3-title').send_keys('s2title')
        b.find_element_by_id('id_-section-3-text').send_keys('s2text')
        b.find_element_by_id('id_-section-4-title').send_keys('s3title')
        b.find_element_by_id('id_-section-4-text').send_keys('s3text')

        # click remove thingie
        b.find_element_by_id('-section-3-remove').click()

        self._submit_and_check(b)

        el = b.find_element_by_xpath('//div[@id="section_1"]//h2')
        self.assertEqual(el.text, '1234')

        el = b.find_element_by_xpath('//div[@id="section_2"]//h2')
        self.assertEqual(el.text, 's3title')

    def test_add_to_existing_sections(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        b.find_element_by_id('id_-section-2-title').send_keys('1234')
        b.find_element_by_id('create_submit').click()

        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))

        add_section = b.find_element_by_id('add_section')
        add_section.click()

        self.assertEqual(len(b.find_elements_by_id('id_-section-3-title')), 1)

        self._submit_and_check(b)

    def _submit_and_check(self, b):
        b.find_element_by_id('create_submit').click()
        self.disable_popups()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote saved.' in success_message.text)
