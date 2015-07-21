from django.core.urlresolvers import reverse
from functional_tests import browser


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
        b.get(self.live_server_url + reverse('client_briefs', args=['client', c.id]))
        b.find_element_by_id('add_client_brief').click()

        # fill out brief & save
        b.find_element_by_name('name').send_keys('Brief test')
        b.find_element_by_xpath('//button[@type="submit"]').click()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Brief Detail', section_title.text)
