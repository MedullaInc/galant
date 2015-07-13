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
        b.find_element_by_name('intro_title').send_keys('test intro title')
        b.find_element_by_name('intro_text').send_keys('test intro text')
        b.find_element_by_name('margin_section_title').send_keys('test margin title')
        b.find_element_by_name('margin_section_text').send_keys('test margin text')
        b.find_element_by_xpath('//select[@name="language"]/option[@value="en"]').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()

        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Quote', h3.text)

    def test_edit_quote(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_quote', args=[1]))

        b.find_element_by_name('intro_title').clear()
        b.find_element_by_name('intro_title').send_keys('modified intro title')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Quote', h3.text)
        intro = b.find_element_by_xpath('//div[@id="intro_section"]/h3[1]/b')
        self.assertEqual(intro.text, 'modified intro title')

    def test_add_sections(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_quote', args=[1]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_section_1_title').send_keys('1234')
        b.find_element_by_id('id_section_1_text').send_keys('1234')
        b.find_element_by_id('id_section_2_title').send_keys('4321')
        b.find_element_by_id('id_section_2_text').send_keys('4321')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Quote', h3.text)
        intro = b.find_element_by_xpath('//div[@id="section_1"]/h3[1]/b')
        self.assertEqual(intro.text, '1234')
        intro = b.find_element_by_xpath('//div[@id="section_2"]/h3[1]/b')
        self.assertEqual(intro.text, '4321')

    def test_section_order(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_quote', args=[1]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_section_1_title').send_keys('1234')
        b.find_element_by_id('id_section_1_text').send_keys('1234')
        b.find_element_by_id('id_section_2_title').send_keys('s2title')
        b.find_element_by_id('id_section_2_text').send_keys('s2text')
        b.find_element_by_id('id_section_3_title').send_keys('s3title')
        b.find_element_by_id('id_section_3_text').send_keys('s3text')

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Quote', h3.text)
        el = b.find_element_by_xpath('//div[@id="section_1"]/h3[1]/b')
        self.assertEqual(el.text, '1234')
        el = b.find_element_by_xpath('//div[@id="section_3"]/h3[1]/b')
        self.assertEqual(el.text, 's3title')

    def test_remove_section(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_quote', args=[1]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        add_section.click()
        add_section.click()
        b.find_element_by_id('id_section_1_title').send_keys('1234')
        b.find_element_by_id('id_section_1_text').send_keys('1234')
        b.find_element_by_id('id_section_2_title').send_keys('s2title')
        b.find_element_by_id('id_section_2_text').send_keys('s2text')
        b.find_element_by_id('id_section_3_title').send_keys('s3title')
        b.find_element_by_id('id_section_3_text').send_keys('s3text')

        # click remove thingie
        b.find_element_by_id('section_2_remove').click()

        b.find_element_by_xpath('//button[@type="submit"]').click()
        h3 = self.browser.find_element_by_tag_name('h3')
        self.assertEqual(u'Quote', h3.text)
        el = b.find_element_by_xpath('//div[@id="section_1"]/h3[1]/b')
        self.assertEqual(el.text, '1234')
        el = b.find_element_by_xpath('//div[@id="section_2"]/h3[1]/b')
        self.assertEqual(el.text, 's3title')

    def test_add_to_existing_sections(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_quote', args=[1]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()
        b.find_element_by_id('id_section_1_title').send_keys('1234')
        b.find_element_by_xpath('//button[@type="submit"]').click()

        b.get(self.live_server_url + reverse('edit_quote', args=[1]))
        self.load_scripts()

        add_section = b.find_element_by_id('add_section')
        add_section.click()

        self.assertEqual(len(b.find_elements_by_id('id_section_1_title')), 1)
