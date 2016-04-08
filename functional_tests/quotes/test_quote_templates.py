from django.core.urlresolvers import reverse
from functional_tests import browser
import autofixture
from unittest import skip
from quotes import models as qm
from selenium.common.exceptions import NoSuchElementException


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


def tearDownModule():
    browser.close()


class QuoteTemplatesTest(browser.SignedInTest):
    def setUp(self):
        super(QuoteTemplatesTest, self).setUp()
        self.disable_popups()

    def test_add_quote_template(self):
        b = browser.instance()

        q = get_blank_quote_autofixture(self.user)
        q.save()

        b.get(self.live_server_url + reverse('add_quote_template'))

        browser.wait().until(lambda driver: driver.find_element_by_id('quote_name')).send_keys('Quote test')
        browser.wait().until(lambda driver: driver.find_element_by_id('service_name_0')).send_keys('1234')
        b.find_element_by_id('quantity_0').send_keys('1')
        b.find_element_by_id('description_0').send_keys('desc')
        b.find_element_by_xpath('//select[@id="type_0"]/option[2]').click()

        b.find_element_by_id('text_0').send_keys('test intro text')
        b.find_element_by_id('title_0').send_keys('test margin title')
        b.find_element_by_id('text_1').send_keys('test intro text')
        b.find_element_by_id('title_1').send_keys('test margin title')

        #b.find_element_by_xpath('//select[@e-name="-service-2-type"]/option[@value="3"]').click()

        self._submit_and_check(b, True)

    def test_add_quote_lang_dropdown(self):
        b = browser.instance()

        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()

        b.get(self.live_server_url + reverse('add_quote_template'))
        browser.wait().until(lambda driver: driver.find_element_by_id('quote_name')).send_keys('New quote')
        b.find_element_by_id('service_name_0').send_keys('1234')
        b.find_element_by_id('quantity_0').send_keys('1')
        b.find_element_by_xpath('//select[@id="type_0"]/option[2]').click()

        #b.find_element_by_xpath('//select[@e-name="-service-2-type"]/option[@value="3"]').click()
        self._add_language_and_text(b, True)

    def test_quote_template_detail(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False,
                                    field_values={'quote': q, 'user': self.user})

        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()

        b.get(self.live_server_url + reverse('quotetemplate_detail', args=[qt.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        b.find_element_by_id('quote_edit').click()
        b.find_element_by_id('quote_name').send_keys('Quote test')

        b.find_element_by_id('title_0').clear()
        b.find_element_by_id('title_0').send_keys('modified intro title')
        b.find_element_by_id('text_0').clear()
        b.find_element_by_id('text_0').send_keys('modified intro title')


        self._submit_and_check(b)

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        b.find_element_by_id('quote_edit').click()
        intro = b.find_element_by_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_delete_quote_template(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False,
                                    field_values={'quote': q, 'user': self.user})

        b.get(self.live_server_url + reverse('delete_quote_template', args=[qt.id]))

        response = self.client.get(self.live_server_url + reverse('quotetemplate_detail', args=[qt.id]))
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_quote_template(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False,
                                    field_values={'quote': q, 'user': self.user})

        b.get(self.live_server_url + reverse('quotetemplate_detail', args=[qt.id]))
        self.disable_popups()

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        with browser.wait_for_page_load():
            b.find_element_by_id('quote_delete').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quotetemplate deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('quotetemplate_detail', args=[qt.id]))
        self.assertEqual(response.status_code, 404)

    def test_edit_quote_lang_dropdown(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False,
                                    field_values={'quote': q, 'user': self.user})

        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        c.save()     

        b.get(self.live_server_url + reverse('quotetemplate_detail', args=[qt.id]))
        browser.wait().until(lambda driver: driver.find_element_by_id('quote_edit')).click()
        b.find_element_by_id('quote_name').send_keys('new quote')
        self._add_language_and_text(b)

    def test_add_from_quote(self):
        b = browser.instance()

        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('add_quote_template', kwargs={'quote_id': q.id}))

        browser.wait().until(lambda driver: driver.find_element_by_id('quote_edit')).click()
        self.assertEqual(q.intro().title, {u'en': u'intro'})

    def test_add_quote_from_template(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False,
                                    field_values={'quote': q, 'user': self.user})
        b.get(self.live_server_url + reverse('add_quote') +
              '?template_id=%d&lang=en&client_id=%d' % (qt.id, q.client.id))
        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        b.find_element_by_id('quote_name').send_keys('new quote')
        with browser.wait_for_page_load():
            b.find_element_by_id('quote_save').click()
        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote saved.' in success_message.text)

    def _add_language_and_text(self, b, redirect=False):
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//*[@e-id="quote_name"]').text != 'empty')
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//*[@e-id="quote_name"]').text != '')
        b.find_element_by_id('title_0').send_keys('test intro title')
        b.find_element_by_id('text_0').send_keys('test intro text')
        b.find_element_by_id('title_1').send_keys('test notes title')
        b.find_element_by_id('text_1').send_keys('test notes text')
        trans_btn = b.find_element_by_id('add_translation_button')
        trans_btn.click()
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//*[@id="id_language"]/option[@label="English"]'))
        b.find_element_by_xpath('//*[@id="id_language"]/option[@label="Spanish"]').click()
        b.find_element_by_id('language_add').click()
        b.find_element_by_id('title_0').clear()
        b.find_element_by_id('title_0').send_keys('titulo de intro prueba')
        b.find_element_by_id('text_0').send_keys('texto de intro prueba')
        b.find_element_by_id('title_1').send_keys('titulo de notas prueba')
        b.find_element_by_id('text_1').send_keys('texto de notas prueba')
        try:
            b.find_element_by_id('service_name_0').send_keys('1234')
        except NoSuchElementException:
            pass
        self._submit_and_check(b, redirect)

        new_tab = browser.wait().until(lambda driver: driver.find_element_by_id('es_tab'))
        self.assertEqual(u'Spanish', new_tab.text)

        b.find_element_by_id('es_tab').click()
        b.find_element_by_id('quote_edit').click()
        intro = b.find_element_by_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'titulo de intro prueba')

    def test_can_access_quote_template_endpoint(self):
        q = get_blank_quote_autofixture(self.user)
        qt = autofixture.create_one('quotes.QuoteTemplate', generate_fk=False,
                                    field_values={'quote': q, 'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api-quote-template-detail', args=[qt.id]))
        self.assertEqual(response.status_code, 200)

    def _submit_and_check(self, b, redirect=False):
        if redirect:
            with browser.wait_for_page_load():
                b.find_element_by_id('quote_save').click()
            success_message = b.find_element_by_class_name('alert-success')
            self.assertTrue(u'Quotetemplate saved.' in success_message.text)
        else:
            b.find_element_by_id('quote_save').click()
            success_message = browser.wait().until(lambda driver: driver.find_element_by_class_name('alert-success'))
            self.assertTrue(u'Saved.' in success_message.text)