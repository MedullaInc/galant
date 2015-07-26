from django.core.urlresolvers import reverse
from functional_tests import browser
import autofixture


def tearDown():
    browser.close()


def get_blank_quote_autofixture():
    i = autofixture.create_one('quotes.Section', generate_fk=True, field_values={'name': 'intro', 'index': 0})
    i.save()
    m = autofixture.create_one('quotes.Section', generate_fk=True, field_values={'name': 'margin', 'index': 1})
    m.save()
    q = autofixture.create_one('quotes.Quote', generate_fk=True, field_values={'sections': [], 'language': 'en'})
    q.sections.add(i)
    q.sections.add(m)
    q.save()
    return q


class QuotesSignedInTest(browser.SignedInTest):
    def test_can_access_quotes(self):
        # check 'Quotes' h1
        browser.instance().get(self.live_server_url + reverse('quotes'))

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual('Quotes', section_title.text)

    def test_add_quote(self):
        b = browser.instance()
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()
        b.get(self.live_server_url + reverse('add_quote'))

        b.find_element_by_name('name').send_keys('Quote test')
        b.find_element_by_xpath('//select[@name="client"]/option[@value="%d"]' % c.id).click()
        b.find_element_by_id('id_-section-0_intro_title').send_keys('test intro title')
        b.find_element_by_id('id_-section-0_intro_text').send_keys('test intro text')
        b.find_element_by_id('id_-section-1_margin_title').send_keys('test margin title')
        b.find_element_by_id('id_-section-1_margin_text').send_keys('test margin text')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Quote', section_title.text)

    def test_edit_quote(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()

        b.find_element_by_id('id_-section-0_intro_title').clear()
        b.find_element_by_id('id_-section-0_intro_title').send_keys('modified intro title')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = b.find_element_by_class_name('section_title')
        self.assertEqual(u'Quote', section_title.text)

        intro = b.find_element_by_xpath('//div[@id="intro"]//h2')
        self.assertEqual(intro.text, 'modified intro title')

    def test_add_sections(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()

        b.find_element_by_id('id_-section-2_section_1_title').send_keys('1234')
        b.find_element_by_id('id_-section-2_section_1_text').send_keys('1234')
        b.find_element_by_id('id_-section-3_section_2_title').send_keys('4321')
        b.find_element_by_id('id_-section-3_section_2_text').send_keys('4321')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = b.find_element_by_class_name('section_title')
        self.assertEqual(u'Quote', section_title.text)

        intro = b.find_element_by_xpath('//div[@id="section_1"]//h2')
        self.assertEqual(intro.text, '1234')

        intro = b.find_element_by_xpath('//div[@id="section_2"]//h2')
        self.assertEqual(intro.text, '4321')

    def test_add_service(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()

        add_service = b.find_element_by_id('add_service')
        add_service.click()

        b.find_element_by_id('id_-service-2_section_1_name').send_keys('1234')
        b.find_element_by_xpath('//select[@name="-service-2_section_1_type"]/option[@value="3"]').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = b.find_element_by_class_name('section_title')
        self.assertEqual(u'Quote', section_title.text)

        name = b.find_element_by_class_name('service_name')
        self.assertEqual(name.text, '1234')

    def test_section_order(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_-section-2_section_1_title').send_keys('1234')
        b.find_element_by_id('id_-section-2_section_1_text').send_keys('1234')
        b.find_element_by_id('id_-section-3_section_2_title').send_keys('s2title')
        b.find_element_by_id('id_-section-3_section_2_text').send_keys('s2text')
        b.find_element_by_id('id_-section-4_section_3_title').send_keys('s3title')
        b.find_element_by_id('id_-section-4_section_3_text').send_keys('s3text')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Quote', section_title.text)

        el = b.find_element_by_xpath('//div[@id="section_1"]//h2')
        self.assertEqual(el.text, '1234')

        el = b.find_element_by_xpath('//div[@id="section_3"]//h2')
        self.assertEqual(el.text, 's3title')

    def test_remove_section(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()
        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_-section-2_section_1_title').send_keys('1234')
        b.find_element_by_id('id_-section-2_section_1_text').send_keys('1234')
        b.find_element_by_id('id_-section-3_section_2_title').send_keys('s2title')
        b.find_element_by_id('id_-section-3_section_2_text').send_keys('s2text')
        b.find_element_by_id('id_-section-4_section_3_title').send_keys('s3title')
        b.find_element_by_id('id_-section-4_section_3_text').send_keys('s3text')

        # click remove thingie
        b.find_element_by_id('-section-3_section_2_remove').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Quote', section_title.text)

        el = b.find_element_by_xpath('//div[@id="section_1"]//h2')
        self.assertEqual(el.text, '1234')

        el = b.find_element_by_xpath('//div[@id="section_2"]//h2')
        self.assertEqual(el.text, 's3title')

    def test_add_to_existing_sections(self):
        b = browser.instance()
        q = get_blank_quote_autofixture()
        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        b.find_element_by_id('id_-section-2_section_1_title').send_keys('1234')
        b.find_element_by_xpath('//button[@type="submit"]').click()

        b.get(self.live_server_url + reverse('edit_quote', args=[q.id]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()

        self.assertEqual(len(b.find_elements_by_id('id_-section-2_section_1_title')), 1)
