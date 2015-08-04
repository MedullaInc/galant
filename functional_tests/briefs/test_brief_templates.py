from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm
import autofixture


def tearDown():
    browser.close()


class BriefTemplatesTest(browser.SignedInTest):
    def test_add_brief_template(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_brief_template'))

        b.find_element_by_name('name').send_keys('Brief test')

        self._submit_and_check(b)

    def test_add_brief_lang_dropdown(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_brief_template'))
        self.load_scripts()

        b.find_element_by_name('name').send_keys('Brief test')
        self._add_language_and_text(b)

        self._submit_and_check(b)

    def test_edit_brief_template(self):
        b = browser.instance()
        quest = bm.Question.objects.create()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True, field_values={'questions': [quest]})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False, field_values={'brief': brief})
        b.get(self.live_server_url + reverse('edit_brief_template', args=[bt.id]))
        self.load_scripts()

        b.find_element_by_id('id_-question-0-question').clear()
        b.find_element_by_id('id_-question-0-question').send_keys('modified question')

        self._submit_and_check(b)
        self.load_scripts()

        intro = b.find_element_by_id('id_-question-0-question')
        self.assertEqual(intro.get_attribute('value'), 'modified question')

    def test_edit_brief_lang_dropdown(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True)
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False, field_values={'brief': brief})
        b.get(self.live_server_url + reverse('edit_brief_template', args=[bt.id]))
        self.load_scripts()
        self._add_language_and_text(b)

    def test_add_from_brief(self):
        b = browser.instance()

        quest = bm.Question.objects.create()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True, field_values={'questions': [quest]})
        b.get(self.live_server_url + reverse('add_brief_template', kwargs={'brief_id': brief.id}))
        self.load_scripts()

        question = b.find_element_by_id('id_-question-0-question_hidden')
        self.assertEqual(quest.question.json(), question.get_attribute('value'))

    def test_add_brief_from_template(self):
        b = browser.instance()
        client = autofixture.create_one('gallant.Client')
        quest = bm.Question.objects.create(question='Who\'s on first?')
        brief = autofixture.create_one('briefs.Brief', generate_fk=True, field_values={'questions': [quest]})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False, field_values={'brief': brief})
        b.get(self.live_server_url +
              reverse('add_brief', args=[client.id]) + '?template_id=%d&lang=en' % bt.id)
        self.load_scripts()

        question = b.find_element_by_id('id_-question-0-question_hidden')
        self.assertEqual(quest.question.json(), question.get_attribute('value'))
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def _add_language_and_text(self, b):
        b.find_element_by_id('add_question').click()
        b.find_element_by_id('id_-question-0-question').clear()
        b.find_element_by_id('id_-question-0-question').send_keys('Who\'s on first?')
        b.find_element_by_id('add_translation_button').click()
        b.find_element_by_xpath('//div[@class="popover-content"]//select[@id="id_language"]/option[@value="es"]').click()
        b.find_element_by_xpath('//div[@class="popover-content"]//button').click()
        b.find_element_by_id('id_-question-0-question').clear()
        b.find_element_by_id('id_-question-0-question').send_keys('Quien esta en primera?')
        b.find_element_by_id('en_tab').click()

        new_tab = b.find_element_by_xpath('//*[@id="es_tab"]/a')
        self.assertEqual(u'Spanish', new_tab.text)

        question = b.find_element_by_xpath('//input[@id="id_-question-0-question"]')
        b.find_element_by_id('es_tab').click()
        self.assertEqual(question.get_attribute('value'), 'Quien esta en primera?')

    def _submit_and_check(self, b):
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Template saved.' in success_message.text)