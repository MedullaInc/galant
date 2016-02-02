# coding=utf-8
from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm
import autofixture


def tearDownModule():
    browser.close()


class BriefsSignedInTest(browser.SignedInTest):
    def setUp(self):
        super(BriefsSignedInTest, self).setUp()

        self.browser = browser.instance()
        self.disable_popups()
        
        c = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'user': self.user, 'client': c, 'quote': None})
        q = bm.TextQuestion.objects.create(user=brief.user, question='What?')
        mq = bm.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                      choices=['a', 'b', 'c'], index=1)
        brief.questions.add(q)
        brief.questions.add(mq)
        
        self.brief = brief 
    
    def test_can_access_briefs(self):
        # check 'Briefs' h1
        browser.instance().get(self.live_server_url + reverse('briefs'))
        h2 = browser.instance().find_element_by_tag_name('h2')
        self.assertIn('Briefs', h2.text)

    def test_add_brief(self):
        b = self.browser

        # access Client Briefs & click add brief
        b.get(self.live_server_url + reverse('briefs') + '?client_id=%s' % self.brief.client.id)
        b.find_element_by_id('add_brief').click()
        b.find_element_by_css_selector('.popover-content .from_scratch_button').click()

        # fill out brief & save
        b.find_element_by_id('id_title').send_keys('Brief test')
        b.find_element_by_id('id_greeting').send_keys('Brief test')
        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')

        self.assertTrue(u'Brief saved.' in success_message.text)


    def test_edit_client_brief(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_brief', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        browser.wait().until(lambda driver: driver.find_element_by_id('question1_question'))
        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')

        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_edit_client_brief_question(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_brief', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        browser.wait().until(lambda driver: driver.find_element_by_id('question1_question'))
        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')

        b.find_element_by_id('question0_question').send_keys('Who is your daddy, and what does he do?')
        b.find_element_by_id('question1_add_choice').click()
        b.find_element_by_id('question1_choice3').send_keys('foo')

        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_add_client_brief_multiquestion(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_brief', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        browser.wait().until(lambda driver: driver.find_element_by_id('question1_question'))
        b.find_element_by_id('add_multiquestion').click()
        b.find_element_by_id('question2_question').send_keys('Who is your daddy, and what does he do?')
        b.find_element_by_id('question2_choice0').send_keys('foo')
        b.find_element_by_id('question2_choice1').send_keys('bar')

        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

        answer = b.find_element_by_xpath('//div[@id="question_2"]/div/div[1]').text
        self.assertEqual(answer, u'— foo')

    def test_client_brief_detail(self):
        b = self.browser
        b.get(self.live_server_url + reverse('brief_detail', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual(u'Brief Detail', app_title.text)

    def test_add_quote_brief(self):
        b = self.browser
        b.get(self.live_server_url + reverse('edit_brief', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        browser.wait().until(lambda driver: driver.find_element_by_id('question1_question'))
        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')
        b.find_element_by_id('id_greeting').send_keys('modified greeting')

        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_add_project_brief(self):
        b = self.browser
        c = self.brief.client
        p = autofixture.create_one('gallant.Project', generate_fk=True,
                                   field_values={'user': self.user})
        autofixture.create_one('quotes.Quote', generate_fk=True,
                               field_values={'user': self.user, 'client': c, 'project': p})

        b.get(self.live_server_url + reverse('add_brief') + '?project_id=%d' % p.id)

        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')
        b.find_element_by_id('id_greeting').send_keys('Brief test')

        with browser.wait_for_page_load():
            b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_send_answers_link(self):
        b = self.browser
        brief = self.brief

        b.get(self.live_server_url + reverse('brief_detail', args=[brief.id]))
        browser.wait().until(lambda driver: driver.find_element_by_id('send_brief'))
        b.find_element_by_id('send_brief').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief link sent to %s.' % brief.client.email in success_message.text)
        brief.refresh_from_db()
        self.assertEqual(brief.status, '2')

    def test_soft_delete_brief(self):
        b = self.browser
        client = self.brief.client
        brief = self.brief

        b.get(self.live_server_url + reverse('delete_brief', args=[brief.id]))

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('brief_detail', args=[brief.id]) + '?client_id=%d' % client.id)
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_brief_template(self):
        b = self.browser
        brief = self.brief

        # Create Template
        template = autofixture.create_one(bm.BriefTemplate, generate_fk=True,
                                          field_values={'user': self.user, 'brief': brief})

        # access delete view
        b.get(self.live_server_url + reverse('delete_brief_template', args=[template.id]))

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('brief_template_detail', args=[template.id]))
        self.assertEqual(response.status_code, 404)

    def test_can_access_brief_endpoint(self):
        response = self.client.get(self.live_server_url + reverse('api-brief-detail', args=[self.brief.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_access_question_endpoint(self):
        question = bm.TextQuestion.objects.create(user=self.user, question='What?')

        response = self.client.get(self.live_server_url + reverse('api_question_detail', args=[question.id]))
        self.assertEqual(response.status_code, 200)

    def test_can_access_question_list(self):

        response = self.client.get(self.live_server_url + reverse('api_questions') +
                                   '?brief_id=%d' % self.brief.id)
        self.assertEqual(response.status_code, 200)

