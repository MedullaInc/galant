from django.core.urlresolvers import reverse
from functional_tests import browser
from quotes import models as qm
from gallant import models as g
from unittest import skip


def tearDownModule():
    browser.close()


class QuotesSignedInTest(browser.SignedInTest):
    def setUp(self):
        super(QuotesSignedInTest, self).setUp()
        c = self.create_one('gallant.Client')
        q = self.create_one('quotes.Quote', {'sections': [], 'services': [], 'language': 'en',
                                             'client': c, 'status': '1'})
        i = qm.Section.objects.create(user=q.user, name='intro', title='intro', text='intro text', index=0)
        m = qm.Section.objects.create(user=q.user, name='important_notes', title='notes', text='notes text', index=1)
        q.sections.add(i)
        q.sections.add(m)
        self.q = q
        self.disable_popups()

    def test_quote_pipeline(self):
        c = self.q.client
        c.auto_pipeine = True
        c.status = g.ClientStatus.Potential.value
        c.save()
        self.q.status = qm.QuoteStatus.Accepted.value
        self.q.save()
        self.assertEqual('Quote Accepted', c.card.alert)

    def test_can_access_quotes(self):
        # check 'Quotes' h1
        self.get(self.live_server_url + reverse('quotes'))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Quotes', app_title.text)

    def test_access_quote_preview(self):
        self.get(self.live_server_url + reverse('quote_preview', args=[self.q.id]))

        page_wrapper = browser.instance().find_element_by_class_name('page-wrapper')
        self.assertTrue(page_wrapper)

    def test_access_quote_header(self):
        self.get(self.live_server_url + reverse('quote_header', args=[self.q.id]))

        header = browser.instance().find_element_by_class_name('header')
        self.assertTrue(header)

    def test_access_quote_footer(self):
        self.get(self.live_server_url + reverse('quote_footer', args=[self.q.id]))

        footer = browser.instance().find_element_by_class_name('footer')
        self.assertTrue(footer)

    def test_access_quote_text_version(self):
        response = self.client.get(self.live_server_url + reverse('quote_txt', args=[self.q.id]))
        self.assertEqual(response.status_code, 200)

    def test_add_quote(self):
        self.get(self.live_server_url + reverse('add_quote'))
        self.e_id('quote_name').send_keys('Quote test')
        self.click_xpath('//select[@name="client"]/option[2]')
        self.e_id('title_0').send_keys('test important notes title')
        self.e_id('text_0').send_keys('test important notes text')
        self.e_id('title_1').send_keys('test important notes title')
        self.e_id('text_1').send_keys('test important notes text')
        self.e_id('service_name_0').send_keys('test service')
        self.e_id('quantity_0').send_keys('2')
        self.click_xpath('//*[@id="type_0"]/option[2]')

        self.click_id('service0_delete')

        self._submit_and_check(True)

    def test_edit_quote(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.click_id('quote_edit')
        self.e_id('quote_name').send_keys('Quote test')
        self.click_xpath('//select[@name="client"]/option[1]')
        self.e_id('title_0').clear()
        self.e_id('title_0').send_keys('modified intro title')
        self.e_id('text_0').send_keys('modified intro text')

        self._submit_and_check()

        self.click_id('quote_edit')
        intro = self.e_id('title_0')
        self.assertEqual(intro.get_attribute('value'), 'modified intro title')

    def test_accept_quote(self):
        self.q.status = 1
        self.q.save()
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.disable_popups()
        self.submit('quote_accept')

        response = self.client.get(
            self.live_server_url + reverse('project_detail', args=[self.q.projects.all_for(self.user)[0].id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_quote(self):
        self.get(self.live_server_url + reverse('delete_quote', args=[self.q.id]))

        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_quote(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.disable_popups()

        self.e_id('section_0')
        self.submit('quote_delete')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Quote deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.assertEqual(response.status_code, 404)

    @skip("TODO")
    def test_email_quote(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))
        self.click_id('send_quote')
        success_message = self.e_class('alert-success')
        self.assertTrue(u'Quote link sent to %s.' % self.q.client.email in success_message.text)
        self.q.refresh_from_db()
        self.assertEqual(self.q.status, '2')
        self.get(self.live_server_url + reverse('client_detail', args=[self.q.client_id]))
        self.assertTrue(self.e_id('note_%s' % self.q.client.notes.all_for(self.user).reverse()[0].id))

    def test_add_sections(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        self.e_id('section_0')
        self.click_id('quote_edit')
        self.click_id('add_section')
        self.e_id('title_2').clear()
        self.e_id('text_2').clear()
        self.e_id('title_2').send_keys('1234')
        self.e_id('text_2').send_keys('4321')

        self._submit_and_check()

        self.click_id('quote_edit')

        self.assertEqual(self.e_id('title_2').get_attribute('value'), '1234')

        self.assertEqual(self.e_id('text_2').get_attribute('value'), '4321')

    def test_add_service(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        self.click_id('quote_edit')
        self.e_id('quote_name').send_keys('Quote test')
        self.click_xpath('//select[@name="client"]/option[1]')

        self.click_id('add_service')
        self.click_xpath('//*[@id="service_from_scratch"]')
        self.e_id('service_name_0').send_keys('1234')
        self.e_id('quantity_0').send_keys('1')
        self.e_id('description_0').send_keys('desc')

        self.click_xpath('//select[@id="type_0"]/option[2]')
        self._submit_and_check()

        name = self.e_css('p[e-id="service_name_0"]')
        self.assertEqual(name.text, '1234')

    def test_remove_section(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        self.disable_angular_popups()

        self.e_id('section_0')
        self.click_id('add_section')
        self.e_id('title_1').clear()
        self.e_id('text_1').clear()
        self.e_id('title_1').send_keys('s1title')
        self.e_id('text_1').send_keys('s1text')
        self.e_id('title_2').send_keys('s2title')
        self.e_id('text_2').send_keys('s2text')

        # click remove thingie
        self.click_id('section0_delete')

        self._submit_and_check()

        self.click_id('quote_edit')

        el = self.e_id('title_0')
        self.assertEqual(el.get_attribute('value'), 's1title')

        el2 = self.e_id('text_0')
        self.assertEqual(el2.get_attribute('value'), 's1text')

    def test_add_to_existing_sections(self):
        self.get(self.live_server_url + reverse('quote_detail', args=[self.q.id]))

        self.e_id('section_0')
        self.click_id('add_section')

        self.assertIsNotNone(self.b.find_elements_by_id('title_2'))
        self.e_id('title_2').send_keys('s2title')
        self.e_id('text_2').send_keys('s2text')

        self._submit_and_check()

    def test_can_access_quote_endpoint(self):
        response = self.client.get(self.live_server_url + reverse('api-quote-detail', args=[self.q.id]))
        self.assertEqual(response.status_code, 200)

    def _submit_and_check(self, redirect=False):
        if redirect:
            self.submit('quote_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Quote saved.' in success_message.text)
        else:
            self.click_id('quote_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Saved.' in success_message.text)
