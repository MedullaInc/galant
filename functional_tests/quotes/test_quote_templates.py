from django.core.urlresolvers import reverse
from functional_tests import browser
import autofixture
from test_quotes import get_blank_quote_autofixture


def tearDown():
    browser.close()


class QuoteTemplatesTest(browser.SignedInTest):
    def test_add_quote_template(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_quote_template'))

        b.find_element_by_name('name').send_keys('Quote test')
        b.find_element_by_id('id_-section-0-title').send_keys('test intro title')
        b.find_element_by_id('id_-section-0-text').send_keys('test intro text')
        b.find_element_by_id('id_-section-1-title').send_keys('test margin title')
        b.find_element_by_id('id_-section-1-text').send_keys('test margin text')

        self._submit_and_check(b)

    def test_add_quote_lang_dropdown(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_quote_template'))
        self.load_scripts()

        b.find_element_by_name('name').send_keys('Quote test')
        self._add_language_and_text(b)

        self._submit_and_check(b)

    def test_edit_quote_template(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False, field_values={'quote': q})
        b.get(self.live_server_url + reverse('edit_quote_template', args=[qt.id]))
        self.load_scripts()

        b.find_element_by_id('id_-section-0-title').clear()
        b.find_element_by_id('id_-section-0-title').send_keys('modified intro title')

        self._submit_and_check(b)
        self.load_scripts()

        intro = b.find_element_by_id('id_-section-0-title')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_edit_quote_lang_dropdown(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False, field_values={'quote': q})
        b.get(self.live_server_url + reverse('edit_quote_template', args=[qt.id]))
        self.load_scripts()
        self._add_language_and_text(b)

    def test_add_from_quote(self):
        b = browser.instance()

        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('add_quote_template', kwargs={'quote_id': q.id}))
        self.load_scripts()

        intro_title = b.find_element_by_id('id_-section-0-title_hidden')
        self.assertEqual(q.intro().title.json(), intro_title.get_attribute('value'))

    def test_add_quote_from_template(self):

        b = browser.instance()
        q = get_blank_quote_autofixture()
        q.intro().title.set_text('en', 'hello')
        q.intro().save()
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False, field_values={'quote': q})
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('add_quote') + '?template_id=%d&lang=en' % qt.id)
        self.load_scripts()

        intro_title = b.find_element_by_id('id_-section-0-title_hidden')
        self.assertEqual(q.intro().title.json(), intro_title.get_attribute('value'))
        b.find_element_by_xpath('//select[@name="client"]/option[@value="%d"]' % c.id).click()
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote saved.' in success_message.text)

    def _add_language_and_text(self, b):
        b.find_element_by_id('id_-section-0-title').clear()
        b.find_element_by_id('id_-section-0-title').send_keys('test intro title')
        b.find_element_by_id('add_translation_button').click()
        b.find_element_by_xpath('//div[@class="popover-content"]//select[@id="id_language"]/option[@value="es"]').click()
        b.find_element_by_xpath('//div[@class="popover-content"]//button').click()
        b.find_element_by_id('id_-section-0-title').clear()
        b.find_element_by_id('id_-section-0-title').send_keys('titulo de intro prueba')
        b.find_element_by_id('en_tab').click()

        self._submit_and_check(b)
        self.load_scripts()

        new_tab = b.find_element_by_xpath('//*[@id="es_tab"]/a')
        self.assertEqual(u'Spanish', new_tab.text)

        intro = b.find_element_by_xpath('//input[@id="id_-section-0-title"]')
        b.find_element_by_id('es_tab').click()
        self.assertEqual(intro.get_attribute('value'), 'titulo de intro prueba')

    def _submit_and_check(self, b):
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Template saved.' in success_message.text)