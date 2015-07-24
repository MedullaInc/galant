from django.core.urlresolvers import reverse
from functional_tests import browser
import autofixture


def tearDown():
    browser.close()


class BriefsSignedInTest(browser.SignedInTest):
    def test_can_access_briefs(self):
        # check 'Briefs' h1
        browser.instance().get(self.live_server_url + reverse('briefs'))
        h2 = browser.instance().find_element_by_tag_name('h2')
        self.assertIn('Briefs', h2.text)

    def test_add_brief(self):
        b = browser.instance()

        # create Client
        c = autofixture.create_one('gallant.Client', generate_fk=True)
        c.save()

        # access Client Briefs & click add brief
        b.get(self.live_server_url + reverse('client_briefs', args=[c.id]))
        b.find_element_by_id('add_client_brief').click()

        # fill out brief & save
        b.find_element_by_name('title').send_keys('Brief test')
        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Brief Detail', section_title.text)

    def test_edit_brief(self):
        b = browser.instance()
        q = autofixture.create_one('briefs.Brief', generate_fk=True)
        b.get(self.live_server_url + reverse('edit_brief', args=['client', q.id]))
        self.load_scripts()

        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Brief Detail', section_title.text)

    def test_brief_detail(self):
        b = browser.instance()
        q = autofixture.create_one('briefs.Brief', generate_fk=True)
        b.get(self.live_server_url + reverse('brief_detail', args=['client', q.id]))
        self.load_scripts()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Brief Detail', section_title.text)
