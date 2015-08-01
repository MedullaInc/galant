from django.core.urlresolvers import reverse
from functional_tests import browser
import autofixture


def tearDown():
    browser.close()


class BriefAnswersTest(browser.BrowserTest):
    def test_can_access_answers(self):
        q = autofixture.create_one('briefs.Question', generate_fk=True)
        mq = autofixture.create_one('briefs.MultipleChoiceQuestion', generate_fk=True)
        brief = autofixture.create_one('briefs.ClientBrief', generate_fk=True, field_values={'status': 2})
        brief.questions.add(q)
        brief.questions.add(mq)
        brief.save()

        browser.instance().get(self.live_server_url + reverse('brief_answer', args=[brief.token.hex]))
        h2 = browser.instance().find_element_by_tag_name('h2')
        self.assertIn('Answer Brief', h2.text)

    def test_post_answers(self):
        b = browser.instance()
        q = autofixture.create_one('briefs.Question', generate_fk=True)
        mq = autofixture.create_one('briefs.MultipleChoiceQuestion', generate_fk=True)
        brief = autofixture.create_one('briefs.ClientBrief', generate_fk=True, field_values={'status': 2})
        brief.questions.add(q)
        brief.questions.add(mq)
        brief.save()

        b.get(self.live_server_url + reverse('brief_answer', args=[brief.token.hex]))

        b.find_element_by_css_selector('input[type="text"]').send_keys('foobar')
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief answered.' in success_message.text)

