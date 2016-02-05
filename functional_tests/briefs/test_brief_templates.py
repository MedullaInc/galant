from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm
import autofixture


def tearDownModule():
    browser.close()


class BriefTemplatesTest(browser.SignedInTest):
    def test_add_brief_template(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_brief_template'))

        b.find_element_by_name('name').send_keys('Brief test')

        self._submit_and_check(b)

    def test_brief_template_detail(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'user': self.user})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})
        b.get(self.live_server_url + reverse('brief_template_detail', args=[bt.id]))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Brief Template Detail', app_title.text)

    def test_add_brief_lang_dropdown(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_brief_template'))

        b.find_element_by_name('name').send_keys('Brief test')

        self._add_language_and_text(b)
        self._submit_and_check(b)

    def test_edit_brief_template(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'questions': [], 'user': self.user})
        quest = bm.TextQuestion.objects.create(user=brief.user)
        brief.questions.add(quest)
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})
        b.get(self.live_server_url + reverse('edit_brief_template', args=[bt.id]))

        b.find_element_by_id('id_-question-0-question').clear()
        b.find_element_by_id('id_-question-0-question').send_keys('modified question')

        self._submit_and_check(b)

        intro = b.find_element_by_id('id_-question-0-question')
        self.assertEqual(intro.get_attribute('value'), 'modified question')

    def test_edit_brief_lang_dropdown(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'user': self.user})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})
        b.get(self.live_server_url + reverse('edit_brief_template', args=[bt.id]))

        self._add_language_and_text(b)
        self._submit_and_check(b)

    def test_add_from_brief(self):
        b = browser.instance()

        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'questions': [], 'user': self.user})
        quest = bm.TextQuestion.objects.create(user=brief.user)
        brief.questions.add(quest)
        b.get(self.live_server_url + reverse('add_brief_template', kwargs={'brief_id': brief.id}))

        question = b.find_element_by_id('id_-question-0-question_hidden')
        self.assertEqual(quest.question.json(), question.get_attribute('value'))

    def test_add_brief_from_template(self):
        b = browser.instance()
        client = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'questions': [], 'user': self.user})
        quest = bm.TextQuestion.objects.create(user=brief.user, question='Who\'s on first?')
        brief.questions.add(quest)
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})
        b.get(self.live_server_url +
              reverse('add_brief') + '?template_id=%d&lang=en&client_id=%d' % (bt.id, client.id))

        browser.wait().until(lambda driver: driver.find_element_by_id('question0_question'))
        question = b.find_element_by_id('question0_question')
        self.assertEqual(quest.question.get_text(), question.get_attribute('value'))

        with browser.wait_for_page_load():
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

        self._submit_and_check(b)

        new_tab = b.find_element_by_xpath('//*[@id="es_tab"]/a')
        self.assertEqual(u'Spanish', new_tab.text)

        question = b.find_element_by_xpath('//input[@id="id_-question-0-question"]')
        b.find_element_by_id('es_tab').click()
        self.assertEqual(question.get_attribute('value'), 'Quien esta en primera?')

    def test_can_access_brief_template_endpoint(self):
        client = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                   field_values={'user': self.user, 'client': client})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})

        response = self.client.get(self.live_server_url + reverse('api-brief-template-detail', args=[bt.id]))
        self.assertEqual(response.status_code, 200)

    def test_soft_delete_brief_template(self):
        b = browser.instance()
        client = autofixture.create_one('gallant.Client', generate_fk=True,
                                   field_values={'user': self.user})
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                   field_values={'user': self.user, 'client': client})
        q = bm.TextQuestion.objects.create(user=brief.user, question='What?')
        brief.questions.add(q)
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})

        b.get(self.live_server_url + reverse('brief_template_detail', args=[bt.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('question_0'))
        with browser.wait_for_page_load():
            b.find_element_by_id('section_delete').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brieftemplate deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('brief_template_detail', args=[bt.id]))
        self.assertEqual(response.status_code, 404)

    def _submit_and_check(self, b):
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Template saved.' in success_message.text)
