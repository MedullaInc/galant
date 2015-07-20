from django.core.urlresolvers import reverse
from functional_tests import browser
import autofixture


def tearDown():
    browser.close()


class QuoteTemplatesTest(browser.SignedInTest):
    def test_add_quote_template(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_quote_template'))

        b.find_element_by_name('name').send_keys('Quote test')
        b.find_element_by_name('intro_title').send_keys('test intro title')
        b.find_element_by_name('intro_text').send_keys('test intro text')
        b.find_element_by_name('margin_section_title').send_keys('test margin title')
        b.find_element_by_name('margin_section_text').send_keys('test margin text')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Template saved.' in success_message.text)

    def test_add_quote_lang_dropdown(self):
        self._add_language_and_text(self.live_server_url + reverse('add_quote_template'))

    def test_edit_quote_template(self):
        b = browser.instance()
        q = autofixture.create_one('quotes.Quote', generate_fk=True, field_values={'sections': [], 'language': 'en'})
        q.save()
        qt = autofixture.create_one('quotes.QuoteTemplate', field_values={'quote': q})
        b.get(self.live_server_url + reverse('edit_quote_template', args=[qt.id]))

        b.find_element_by_name('intro_title').clear()
        b.find_element_by_name('intro_title').send_keys('modified intro title')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Template saved.' in success_message.text)

        intro = b.find_element_by_xpath('//input[@id="id_intro"]')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_edit_quote_lang_dropdown(self):
        q = autofixture.create_one('quotes.Quote', generate_fk=True, field_values={'sections': [], 'language': 'en'})
        q.save()
        qt = autofixture.create_one('quotes.QuoteTemplate', field_values={'quote': q})
        self._add_language_and_text(self.live_server_url + reverse('edit_quote_template', args=[qt.id]))

    def _add_language_and_text(self, url):
        b = browser.instance()
        b.get(url)
        self.load_scripts()

        b.find_element_by_name('intro_title').clear()
        b.find_element_by_name('intro_title').send_keys('test intro title')
        b.find_element_by_id('add_translation_button').click()
        b.find_element_by_xpath('//select[@id="id_language"]/option[@value="es"]').click()
        b.find_element_by_id('language_add').click()
        b.find_element_by_name('intro_title').clear()
        b.find_element_by_name('intro_title').send_keys('titulo de intro prueba')
        b.find_element_by_id('en_tab').click()

        new_tab = b.find_element_by_xpath('//*[@id="es_tab"]/a')
        self.assertEqual(u'Spanish', new_tab.text)

        intro = b.find_element_by_xpath('//input[@id="id_intro"]')
        b.find_element_by_id('es_tab').click()
        self.assertEqual(intro.get_attribute('value'), 'titulo de intro prueba')