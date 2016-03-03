import time
from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
import autofixture
from unittest import skip


def tearDownModule():
    browser.close()


def get_blank_quote_autofixture(user):
    c = autofixture.create_one('gallant.Client', generate_fk=True,
                               field_values={'user': user})
    q = autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'sections': [],'services': [], 'language': 'en',
                                             'user': user, 'client': c, 'status': '1'})
    i = qm.Section.objects.create(user=q.user, name='intro', index=0)
    m = qm.Section.objects.create(user=q.user, name='important_notes', index=1)
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
                                   field_values={'user': self.user, 'status': '1'})
        c.save()
        b.get(self.live_server_url + reverse('add_quote'))
        browser.wait().until(lambda driver: driver.find_element_by_id('quote_name')).send_keys('Quote test')
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//select[@name="client"]/option[1]'))
        b.find_element_by_xpath('//select[@name="client"]/option[2]').click()
        b.find_element_by_id('quote_save').click()
        b.find_element_by_id('title_0').send_keys('test important notes title')
        b.find_element_by_id('text_0').send_keys('test important notes text')
        b.find_element_by_id('section0_save').click()
        b.find_element_by_id('title_1').send_keys('test important notes title')
        b.find_element_by_id('text_1').send_keys('test important notes text')
        b.find_element_by_id('section1_save').click()

        b.find_element_by_id('service0_save').click()
        b.find_element_by_id('service0_delete').click()

        self._submit_and_check(b)

    def test_edit_quote(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user, 'status': '0'})
        c.save()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))
        browser.wait().until(lambda driver: driver.find_element_by_id('quote_edit')).click()
        b.find_element_by_id('quote_name').send_keys('Quote test')
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//select[@name="client"]/option[1]'))
        b.find_element_by_xpath('//select[@name="client"]/option[2]').click()
        b.find_element_by_id('quote_save').click()
        browser.wait().until(lambda driver: driver.find_element_by_id('section0_edit')).click()
        b.find_element_by_id('title_0').clear()
        b.find_element_by_id('title_0').send_keys('modified intro title')
        b.find_element_by_id('section0_save').click()

        self._submit_and_check(b)

        browser.wait().until(lambda driver: driver.find_element_by_id('section0_edit')).click()
        intro = b.find_element_by_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_delete_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('delete_quote', args=[q.id]))

        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[q.id]))
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_quote(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user, 'status': '0'})
        c.save()
        q = get_blank_quote_autofixture(self.user)

        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))
        self.disable_popups()

        browser.wait().until(lambda driver: driver.find_element_by_id('section1_edit'))
        with browser.wait_for_page_load():
            b.find_element_by_id('quote_delete').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[q.id]))
        self.assertEqual(response.status_code, 404)

    @skip("TODO")
    def test_email_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))
        b.find_element_by_id('send_quote').click()
        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote link sent to %s.' % q.client.email in success_message.text)
        q.refresh_from_db()
        self.assertEqual(q.status, '2')

    def test_add_sections(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        browser.wait().until(lambda driver: driver.find_element_by_id('section1_edit')).click()
        b.find_element_by_id('title_1').send_keys('1234')
        b.find_element_by_id('text_1').send_keys('4321')
        b.find_element_by_id('section1_save').click()

        self._submit_and_check(b)

        browser.wait().until(lambda driver: driver.find_element_by_id('section1_edit'))
        b.find_element_by_id('section1_edit').click()

        self.assertEqual(b.find_element_by_id('title_1').get_attribute('value'), '1234')

        self.assertEqual(b.find_element_by_id('text_1').get_attribute('value'), '4321')

    def test_add_service(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)

        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user, 'status': '1'})
        c.save()
        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('quote_edit')).click()
        b.find_element_by_id('quote_name').send_keys('Quote test')
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//select[@name="client"]/option[1]')).click()
        b.find_element_by_id('quote_save').click()

        b.find_element_by_id('add_service').click()
        b.find_element_by_xpath('//*[@id="service_from_scratch"]').click()
        b.find_element_by_id('service_name_0').send_keys('1234')
        b.find_element_by_id('quantity_0').send_keys('1')
        b.find_element_by_id('description_0').send_keys('desc')

        browser.wait().until(lambda driver: driver.find_element_by_xpath('//select[@id="type_0"]/option[2]')).click()
        b.find_element_by_id('service0_save').click()
        self._submit_and_check(b)

        browser.wait().until(lambda driver: driver.find_element_by_id('section0_edit'))
        name = b.find_element_by_css_selector('p[e-id="service_name_0"]')
        self.assertEqual(name.text, '1234')

    def test_remove_section(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)
        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('add_section'))
        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        browser.wait().until(lambda driver: driver.find_element_by_id('section0_edit')).click()
        browser.wait().until(lambda driver: driver.find_element_by_id('section1_edit')).click()
        b.find_element_by_id('title_0').send_keys('s2title')
        b.find_element_by_id('text_0').send_keys('s2text')
        b.find_element_by_id('title_1').send_keys('s2title')
        b.find_element_by_id('text_1').send_keys('s2text')

        b.find_element_by_id('section0_save').click()
        b.find_element_by_id('section1_save').click()

        # click remove thingie
        b.find_element_by_id('section1_delete').click()

        self._submit_and_check(b)

        browser.wait().until(lambda driver: driver.find_element_by_id('section0_edit')).click()

        el = b.find_element_by_id('title_0')
        self.assertEqual(el.get_attribute('value'), 's2title')

        el2 = b.find_element_by_id('text_0')
        self.assertEqual(el2.get_attribute('value'), 's2text')

    def test_add_to_existing_sections(self):
        b = browser.instance()
        q = get_blank_quote_autofixture(self.user)

        b.get(self.live_server_url + reverse('quote_detail', args=[q.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section0_edit'))
        add_section = b.find_element_by_id('add_section')
        add_section.click()

        self.assertIsNotNone(b.find_elements_by_id('title_2'))
        b.find_element_by_id('title_2').send_keys('s2title')
        b.find_element_by_id('text_2').send_keys('s2text')
        b.find_element_by_id('section2_save').click()

        self._submit_and_check(b)

    def test_can_access_quote_endpoint(self):
        q = get_blank_quote_autofixture(self.user)

        response = self.client.get(self.live_server_url + reverse('api-quote-detail', args=[q.id]))
        self.assertEqual(response.status_code, 200)

    def _submit_and_check(self, b):
        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@id="create_submit"]').click()
        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote saved.' in success_message.text)
