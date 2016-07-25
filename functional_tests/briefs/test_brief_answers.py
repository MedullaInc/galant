from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm


def tearDownModule():
    browser.close()


class BriefAnswersTest(browser.BrowserTest):
    def setUp(self):
        super(BriefAnswersTest, self).setUp()

        brief = self.create_one('briefs.Brief', {'status': 2})
        q = bm.TextQuestion.objects.create(user=brief.user, question='What?')
        brief.questions.add(q)
        self.brief = brief

    def test_can_access_answers(self):
        self.get(self.live_server_url + reverse('brief_answer', args=[self.brief.token.hex]))
        app_title = self.e_class('app_title')
        self.assertIn('Answer Brief', app_title.text)

    def test_post_answers(self):
        self.brief.questions.add(bm.MultipleChoiceQuestion.objects.create(user=self.brief.user, question='Huh?',
                                                                          choices=['a', 'b', 'c'], index=1))
        self.get(self.live_server_url + reverse('brief_answer', args=[self.brief.token.hex]))

        self.e_css('input[type="text"]').send_keys('foobar')
        self.e_css('input[type="radio"][value="1"]').click()
        self.click_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Brief answered.' in success_message.text)

    def test_post_answers_multiselect(self):
        self.brief.questions.add(bm.MultipleChoiceQuestion.objects.create(user=self.brief.user, question='Huh?',
                                                                          choices=['a', 'b', 'c'], index=1,
                                                                          can_select_multiple=True))
        self.get(self.live_server_url + reverse('brief_answer', args=[self.brief.token.hex]))

        self.e_css('input[type="text"]').send_keys('foobar')
        self.e_css('input[type="checkbox"][value="1"]').click()
        self.click_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Brief answered.' in success_message.text)
