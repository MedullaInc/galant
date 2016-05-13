from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
from unittest import skip


def tearDownModule():
    browser.close()


class QuotesSignedInTest(browser.SignedInTest):
    def setUp(self):
        super(QuotesSignedInTest, self).setUp()
        c = self.create_one('gallant.Client')
        q = self.create_one('quotes.Quote', {'sections': [],'services': [], 'language': 'en',
                                             'client': c, 'status': '1'})
        i = qm.Section.objects.create(user=q.user, name='intro', title='intro', text='intro text', index=0)
        m = qm.Section.objects.create(user=q.user, name='important_notes', title='notes', text='notes text', index=1)
        q.sections.add(i)
        q.sections.add(m)
        self.q = q
        self.disable_popups()

    def test_can_access_quotes(self):
        # check 'Quotes' h1
        browser.instance().get(self.live_server_url + reverse('quotes'))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Quotes', app_title.text)

    def test_access_quote_preview(self):
        browser.instance().get(self.live_server_url + reverse('quote_preview', args=[self.q.id]))

        page_wrapper = browser.instance().find_element_by_class_name('page-wrapper')
        self.assertTrue(page_wrapper)

    def test_access_quote_header(self):
        browser.instance().get(self.live_server_url + reverse('quote_header', args=[self.q.id]))

        header = browser.instance().find_element_by_class_name('header')
        self.assertTrue(header)

    def test_access_quote_footer(self):
        browser.instance().get(self.live_server_url + reverse('quote_footer', args=[self.q.id]))

        footer = browser.instance().find_element_by_class_name('footer')
        self.assertTrue(footer)

    def test_add_quote(self):
        b = browser.instance()
        c = self.create_one('gallant.Client', {'status': '1'})
        c.save()
        b.get(self.live_server_url + reverse('add_quote'))
        browser.wait().until(lambda driver: driver.find_element_by_id('quote_name')).send_keys('Quote test')
        browser.wait().until_click(lambda driver: driver.find_element_by_xpath('//select[@name="client"]/option[2]'))
        b.find_element_by_id('title_0').send_keys('test important notes title')
        b.find_element_by_id('text_0').send_keys('test important notes text')
        b.find_element_by_id('title_1').send_keys('test important notes title')
        b.find_element_by_id('text_1').send_keys('test important notes text')
        b.find_element_by_id('service_name_0').send_keys('test service')
        b.find_element_by_id('quantity_0').send_keys('2')
        b.find_element_by_xpath('//*[@id="type_0"]/option[2]').click()

        b.find_element_by_id('service0_delete').click()

        self._submit_and_check(b, True)

    def test_edit_quote(self):
        b = browser.instance()
        c = self.create_one('gallant.Client', {'status': '0'})
        c.save()
        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        browser.wait().until_click(lambda driver: driver.find_element_by_id('quote_edit'))
        b.find_element_by_id('quote_name').send_keys('Quote test')
        browser.wait().until_click(lambda driver: driver.find_element_by_xpath('//select[@name="client"]/option[2]'))
        b.find_element_by_id('title_0').clear()
        b.find_element_by_id('title_0').send_keys('modified intro title')
        b.find_element_by_id('text_0').send_keys('modified intro text')

        self._submit_and_check(b)

        browser.wait().until_click(lambda driver: driver.find_element_by_id('quote_edit'))
        intro = b.find_element_by_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_delete_quote(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('delete_quote', args=[self.q.id]))

        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_quote(self):
        b = browser.instance()
        c = self.create_one('gallant.Client', {'status': '0'})
        c.save()

        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.disable_popups()

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        with browser.wait_for_page_load():
            b.find_element_by_id('quote_delete').click()

        success_message = browser.wait().until(lambda d: d.find_element_by_class_name('alert-success'))
        self.assertTrue(u'Quote deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.assertEqual(response.status_code, 404)

    @skip("TODO")
    def test_email_quote(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        b.find_element_by_id('send_quote').click()
        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Quote link sent to %s.' % self.q.client.email in success_message.text)
        self.q.refresh_from_db()
        self.assertEqual(self.q.status, '2')
        b.get(self.live_server_url + reverse('client_detail', args=[self.q.client_id]))
        self.assertTrue(b.find_element_by_id('note_%s' % self.q.client.notes.all_for(self.user).reverse()[0].id))

    def test_add_sections(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        b.find_element_by_id('quote_edit').click()
        add_section = b.find_element_by_id('add_section')
        add_section.click()
        browser.wait().until(lambda driver: driver.find_element_by_id('title_2')).clear()
        b.find_element_by_id('text_2').clear()
        b.find_element_by_id('title_2').send_keys('1234')
        b.find_element_by_id('text_2').send_keys('4321')

        self._submit_and_check(b)

        browser.wait().until_click(lambda driver: driver.find_element_by_id('quote_edit'))

        self.assertEqual(b.find_element_by_id('title_2').get_attribute('value'), '1234')

        self.assertEqual(b.find_element_by_id('text_2').get_attribute('value'), '4321')

    def test_add_service(self):
        b = browser.instance()

        c = self.create_one('gallant.Client', {'status': '1'})
        c.save()
        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        browser.wait().until_click(lambda driver: driver.find_element_by_id('quote_edit'))
        b.find_element_by_id('quote_name').send_keys('Quote test')
        browser.wait().until_click(lambda driver: driver.find_element_by_xpath('//select[@name="client"]/option[1]'))

        b.find_element_by_id('add_service').click()
        b.find_element_by_xpath('//*[@id="service_from_scratch"]').click()
        b.find_element_by_id('service_name_0').send_keys('1234')
        b.find_element_by_id('quantity_0').send_keys('1')
        b.find_element_by_id('description_0').send_keys('desc')

        browser.wait().until_click(lambda driver: driver.find_element_by_xpath('//select[@id="type_0"]/option[2]'))
        self._submit_and_check(b)

        name = browser.wait().until(lambda driver: driver.find_element_by_css_selector('p[e-id="service_name_0"]'))
        self.assertEqual(name.text, '1234')

    def test_remove_section(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        self.disable_angular_popups(b)

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        add_section = b.find_element_by_id('add_section')
        add_section.click()
        b.find_element_by_id('title_1').clear()
        b.find_element_by_id('text_1').clear()
        b.find_element_by_id('title_1').send_keys('s1title')
        b.find_element_by_id('text_1').send_keys('s1text')
        b.find_element_by_id('title_2').send_keys('s2title')
        b.find_element_by_id('text_2').send_keys('s2text')

        # click remove thingie
        b.find_element_by_id('section0_delete').click()

        self._submit_and_check(b)

        browser.wait().until_click(lambda driver: driver.find_element_by_id('quote_edit'))

        el = b.find_element_by_id('title_0')
        self.assertEqual(el.get_attribute('value'), 's1title')

        el2 = b.find_element_by_id('text_0')
        self.assertEqual(el2.get_attribute('value'), 's1text')

    def test_add_to_existing_sections(self):
        b = browser.instance()

        b.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('section_0'))
        add_section = b.find_element_by_id('add_section')
        add_section.click()

        self.assertIsNotNone(b.find_elements_by_id('title_2'))
        b.find_element_by_id('title_2').send_keys('s2title')
        b.find_element_by_id('text_2').send_keys('s2text')

        self._submit_and_check(b)

    def test_can_access_quote_endpoint(self):

        response = self.client.get(self.live_server_url + reverse('api-quote-detail', args=[self.q.id]))
        self.assertEqual(response.status_code, 200)

    def _submit_and_check(self, b, redirect=False):
        if redirect:
            with browser.wait_for_page_load():
                b.find_element_by_id('quote_save').click()
            success_message = b.find_element_by_class_name('alert-success')
            self.assertTrue(u'Quote saved.' in success_message.text)
        else:
            b.find_element_by_id('quote_save').click()
            success_message = browser.wait().until(lambda driver: driver.find_element_by_class_name('alert-success'))
            self.assertTrue(u'Saved.' in success_message.text)
