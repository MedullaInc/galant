from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
from selenium.common.exceptions import NoSuchElementException


def tearDownModule():
    browser.close()


class QuoteTemplatesTest(browser.SignedInTest):
    def setUp(self):
        super(QuoteTemplatesTest, self).setUp()
        c = self.create_one('gallant.Client')
        q = self.create_one('quotes.Quote', {'sections': [],'services': [], 'language': 'en',
                                             'client': c, 'status': '1'})
        qt = self.create_one('quotes.QuoteTemplate', {'quote': q})
        i = qm.Section.objects.create(user=q.user, name='intro', title='intro', text='intro text', index=0)
        m = qm.Section.objects.create(user=q.user, name='important_notes', title='notes', text='notes text', index=1)
        q.sections.add(i)
        q.sections.add(m)
        self.q = q
        self.qt = qt
        self.disable_popups()

    def test_add_quote_template(self):
        self.get(self.live_server_url + reverse('add_quote_template'))

        self.e_id('quote_name').send_keys('Quote test')
        self.e_id('service_name_0').send_keys('1234')
        self.e_id('quantity_0').send_keys('1')
        self.e_id('description_0').send_keys('desc')
        self.click_xpath('//select[@id="type_0"]/option[2]')

        self.e_id('text_0').send_keys('test intro text')
        self.e_id('title_0').send_keys('test margin title')
        self.e_id('text_1').send_keys('test intro text')
        self.e_id('title_1').send_keys('test margin title')

        self._submit_and_check(True)

    def test_add_quote_lang_dropdown(self):
        self.get(self.live_server_url + reverse('add_quote_template'))
        self.e_id('quote_name').send_keys('New quote')
        self.e_id('service_name_0').send_keys('1234')
        self.e_id('quantity_0').send_keys('1')
        self.click_xpath('//select[@id="type_0"]/option[2]')

        self._add_language_and_text(True)

    def test_quote_template_detail(self):
        self.get(self.live_server_url + reverse('quotetemplate_detail', args=[self.qt.id]))

        self.e_id('section_0')
        self.click_id('quote_edit')
        self.e_id('quote_name').send_keys('Quote test')

        self.e_id('title_0').clear()
        self.e_id('title_0').send_keys('modified intro title')
        self.e_id('text_0').clear()
        self.e_id('text_0').send_keys('modified intro title')

        self._submit_and_check()

        self.click_id('quote_edit')
        intro = self.e_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_delete_quote_template(self):
        self.get(self.live_server_url + reverse('delete_quote_template', args=[self.qt.id]))

        response = self.client.get(self.live_server_url + reverse('quotetemplate_detail', args=[self.qt.id]))
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_quote_template(self):
        self.get(self.live_server_url + reverse('quotetemplate_detail', args=[self.qt.id]))
        self.disable_popups()

        self.submit('quote_delete')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Quotetemplate deleted.' in success_message.text)

        # check that quotetemplate access returns 404
        response = self.client.get(self.live_server_url + reverse('quotetemplate_detail', args=[self.qt.id]))
        self.assertEqual(response.status_code, 404)

    def test_edit_quote_lang_dropdown(self):
        self.get(self.live_server_url + reverse('quotetemplate_detail', args=[self.qt.id]))
        self.click_id('quote_edit')
        self.e_id('quote_name').send_keys('new quote')
        self._add_language_and_text()

    def test_add_from_quote(self):
        self.get(self.live_server_url + reverse('add_quote_template', kwargs={'quote_id': self.q.id}))

        browser.wait().until(lambda driver: driver.find_element_by_id('quote_save').is_displayed)
        self.assertEqual(self.q.intro().title, {u'en': u'intro'})

    def test_add_quote_from_template(self):
        self.get(self.live_server_url + reverse('add_quote') +
              '?template_id=%d&lang=en&client_id=%d' % (self.qt.id, self.q.client.id))
        self.e_id('section_0')
        self.e_id('quote_name').send_keys('new quote')
        self.submit('quote_save')
        success_message = self.e_class('alert-success')
        self.assertTrue(u'Quote saved.' in success_message.text)

    def _add_language_and_text(self, redirect=False):
        self.e_id('title_0').send_keys('test intro title')
        self.e_id('text_0').send_keys('test intro text')
        self.e_id('title_1').send_keys('test notes title')
        self.e_id('text_1').send_keys('test notes text')
        self.click_id('add_translation_button')
        self.e_xpath('//*[@id="id_language"]/option[@label="English"]')
        self.click_xpath('//*[@id="id_language"]/option[@label="Spanish"]')
        self.click_id('language_add')
        self.e_id('title_0').clear()
        self.e_id('title_0').send_keys('titulo de intro prueba')
        self.e_id('text_0').send_keys('texto de intro prueba')
        self.e_id('title_1').send_keys('titulo de notas prueba')
        self.e_id('text_1').send_keys('texto de notas prueba')
        try:
            self.b.find_element_by_id('service_name_0').send_keys('1234')
        except NoSuchElementException:
            pass
        self._submit_and_check(redirect)

        new_tab = self.e_id('es_tab')
        self.assertEqual(u'Spanish', new_tab.text)

        self.click_id('es_tab')
        self.click_id('quote_edit')
        intro = self.e_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'titulo de intro prueba')

    def test_can_access_quote_template_endpoint(self):
        response = self.client.get(self.live_server_url + reverse('api-quote-template-detail', args=[self.qt.id]))
        self.assertEqual(response.status_code, 200)

    def _submit_and_check(self, redirect=False):
        if redirect:
            self.submit('quote_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Quotetemplate saved.' in success_message.text)
        else:
            self.click_id('quote_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Saved.' in success_message.text)