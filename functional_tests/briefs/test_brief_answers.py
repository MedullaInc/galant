from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm
import autofixture


def tearDown():
    browser.close()


class BriefAnswersTest(browser.BrowserTest):
    def test_can_access_answers(self):
        brief = autofixture.create_one('briefs.Brief', generate_fk=True, field_values={'status': 2})
        q = bm.TextQuestion.objects.create(user=brief.user, question='What?')
        mq = bm.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                      choices=['a', 'b', 'c'], index=1)
        brief.questions.add(q)
        brief.questions.add(mq)

        browser.instance().get(self.live_server_url + reverse('brief_answer', args=[brief.token.hex]))
        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertIn('Answer Brief', app_title.text)

    def test_post_answers(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True, field_values={'status': 2})
        q = bm.TextQuestion.objects.create(user=brief.user, question='What?')
        mq = bm.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                      choices=['a', 'b', 'c'], index=1)
        brief.questions.add(q)
        brief.questions.add(mq)
        brief.save()

        b.get(self.live_server_url + reverse('brief_answer', args=[brief.token.hex]))

        b.find_element_by_css_selector('input[type="text"]').send_keys('foobar')
        b.find_element_by_css_selector('input[type="radio"][value="1"]').click()
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief answered.' in success_message.text)

    def test_post_answers_multiselect(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True, field_values={'status': 2})
        q = bm.TextQuestion.objects.create(user=brief.user, question='What?')
        mq = bm.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?', choices=['a', 'b', 'c'],
                                                      index=1, can_select_multiple=True)
        brief.questions.add(q)
        brief.questions.add(mq)
        brief.save()

        b.get(self.live_server_url + reverse('brief_answer', args=[brief.token.hex]))

        b.find_element_by_css_selector('input[type="text"]').send_keys('foobar')
        b.find_element_by_css_selector('input[type="checkbox"][value="1"]').click()
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief answered.' in success_message.text)
