# coding=utf-8
from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm


def tearDownModule():
    browser.close()


class BriefsSignedInTest(browser.SignedInTest):
    def setUp(self):
        super(BriefsSignedInTest, self).setUp()

        self.browser = browser.instance()
        self.disable_popups()
        
        c = self.create_one('gallant.Client')
        brief = self.create_one('briefs.Brief', {'client': c, 'quote': None,
                                                 'status': bm.BriefStatus.Draft.value})
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
        # add brief
        self.get(self.live_server_url + reverse('add_brief') + '?client_id=%s' % self.brief.client.id)

        # fill out brief & save
        self.e_id('brief_title').send_keys('Brief test')
        self.e_id('brief_greeting').send_keys('Brief test')
        self._submit_and_check(True)

    def test_edit_client_brief(self):
        self.get(self.live_server_url + reverse('brief_detail', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        self.click_id('brief_edit')
        self.e_id('brief_title').send_keys('Brief test')
        self.e_id('brief_greeting').send_keys('Brief test')
        self._submit_and_check()

    def test_edit_client_brief_question(self):
        self.get(self.live_server_url + reverse('brief_detail', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        self.click_id('brief_edit')
        self.e_id('question0_question').send_keys('Who is your daddy, and what does he do?')

        self.click_id('question1_add_choice')
        self.e_id('question1_choice3').send_keys('foo')
        self._submit_and_check()

    def test_add_client_brief_multiquestion(self):
        self.get(self.live_server_url + reverse('brief_detail', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        browser.wait().until(lambda driver: driver.find_element_by_id('question0'))
        self.click_id('add_multiquestion')
        self.e_id('question2_question').send_keys('Who is your daddy, and what does he do?')
        self.e_id('question2_choice0').send_keys('foo')
        self.e_id('question2_choice1').send_keys('bar')
        self._submit_and_check()

        el = browser.wait().until(lambda driver:
                                  driver.find_element_by_xpath('//p[@e-id="question2_choice0"]'))
        answer = el.text
        self.assertEqual(answer, u'- foo')

    def test_client_brief_detail(self):
        self.get(self.live_server_url + reverse('brief_detail', args=[self.brief.id]) +
              '?client_id=%d' % self.brief.client.id)

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual(u'Brief Detail', app_title.text)

    def test_add_quote_brief(self):
        c = self.create_one('gallant.Client')
        q = self.create_one('quotes.Quote', {'client': c})

        self.get(self.live_server_url + reverse('brief_detail', args=[self.brief.id]) +
              '?quote_id=%d' % q.id)

        browser.wait().until(lambda driver: driver.find_element_by_id('brief_edit')).click()
        self.e_id('brief_title').send_keys('Brief test')
        self.e_id('brief_greeting').send_keys('Brief test')
        self._submit_and_check()

    def test_add_project_brief(self):
        c = self.brief.client
        p = self.create_one('gallant.Project')
        self.create_one('quotes.Quote', {'client': c, 'project': p})

        self.get(self.live_server_url + reverse('add_brief') + '?project_id=%d' % p.id)
        
        browser.wait().until(lambda driver: driver.find_element_by_id('brief_save'))
        self.e_id('brief_title').send_keys('Brief test')
        self.e_id('brief_greeting').send_keys('Brief test')
        self._submit_and_check(True)

    def test_send_answers_link(self):
        brief = self.brief
        self.get(self.live_server_url + reverse('brief_detail', args=[brief.id]))
        browser.wait().until(lambda driver: driver.find_element_by_id('send_brief'))

        self.submit('send_brief')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Brief link sent to %s.' % brief.client.email in success_message.text)
        brief.refresh_from_db()
        self.assertEqual(brief.status, '2')

    def test_soft_delete_brief(self):
        client = self.brief.client
        brief = self.brief

        self.get(self.live_server_url + reverse('brief_detail', args=[brief.id]))
        self.disable_popups()

        self.e_id('question0')
        self.submit('brief_delete')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Brief deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('brief_detail', args=[brief.id]) + '?client_id=%d' % client.id)
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

    def test_can_access_brief_answers_endpoint(self):
        brief_answers = self.create_one('briefs.BriefAnswers')
        response = self.client.get(self.live_server_url + reverse('api-briefanswers-detail', args=[brief_answers.id]))
        self.assertEqual(response.status_code, 200)

    def _submit_and_check(self, redirect=False):
        if redirect:
            self.submit('brief_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Brief saved.' in success_message.text)
        else:
            self.click_id('brief_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Saved.' in success_message.text)
