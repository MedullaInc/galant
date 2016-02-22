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

        browser.wait().until(lambda driver: driver.find_element_by_id('edit_brief')).click()
        b.find_element_by_id('brief_title').send_keys('Brief test')
        b.find_element_by_id('brief_greeting').send_keys('Brief test')
        b.find_element_by_id('save_edit').click()

        self._submit_and_check(b)

    def test_brieftemplate_detail(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'user': self.user})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})
        b.get(self.live_server_url + reverse('brieftemplate_detail', args=[bt.id]))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Brief Template Detail', app_title.text)

    def test_add_brief_lang_dropdown(self):
        b = browser.instance()
        b.get(self.live_server_url + reverse('add_brief_template'))

        browser.wait().until(lambda driver: driver.find_element_by_id('edit_brief')).click()
        b.find_element_by_id('brief_title').send_keys('Brief test')
        b.find_element_by_id('brief_greeting').send_keys('Brief test')
        b.find_element_by_id('save_edit').click()

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
        b.get(self.live_server_url + reverse('brieftemplate_detail', args=[bt.id]))

        browser.wait().until(lambda driver: driver.find_element_by_id('question0_edit')).click()
        b.find_element_by_id('question0_question').clear()
        b.find_element_by_id('question0_question').send_keys('modified question')
        b.find_element_by_id('question0_save').click()

        self._submit_and_check(b)

        quest = browser.wait().until(lambda driver:
                                     driver.find_element_by_xpath('//span[@e-id="question0_question"]'))
        self.assertEqual(quest.text, 'modified question')

    def test_edit_brief_lang_dropdown(self):
        b = browser.instance()
        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'user': self.user})
        bt = autofixture.create_one('briefs.BriefTemplate', generate_fk=False,
                                    field_values={'brief': brief, 'user': self.user})
        b.get(self.live_server_url + reverse('brieftemplate_detail', args=[bt.id]))

        self._add_language_and_text(b)
        self._submit_and_check(b)

    def test_add_from_brief(self):
        b = browser.instance()

        brief = autofixture.create_one('briefs.Brief', generate_fk=True,
                                       field_values={'questions': [], 'user': self.user})
        quest = bm.TextQuestion.objects.create(user=brief.user)
        brief.questions.add(quest)
        b.get(self.live_server_url + reverse('add_brief_template') + '?brief_id=%d' % brief.id)

        question = browser.wait().until(lambda driver:
                                        driver.find_element_by_xpath('//span[@e-id="question0_question"]'))
        self.assertEqual('empty', question.text)

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

        browser.wait().until(lambda driver: driver.find_element_by_id('question0'))
        question = b.find_element_by_xpath('//span[@e-id="question0_question"]')
        self.assertEqual(quest.question.get_text(), question.text)

        with browser.wait_for_page_load():
            b.find_element_by_id('create_submit').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def _add_language_and_text(self, b):
        browser.wait().until(lambda driver: driver.find_element_by_xpath('//span[@e-id="brief_title"]').text != 'empty')
        b.find_element_by_id('add_question').click()
        b.find_element_by_id('question0_edit').click()
        b.find_element_by_id('question0_question').clear()
        b.find_element_by_id('question0_question').send_keys('Who\'s on first?')
        b.find_element_by_id('question0_save').click()
        b.find_element_by_id('add_translation_button').click()
        b.find_element_by_xpath('//select[@id="id_language"]/option[text()[1]="Spanish"]').click()
        b.find_element_by_id('language_add').click()
        b.find_element_by_xpath('//*[@id="es_tab"]/a').click()
        b.find_element_by_id('question0_edit').click()
        b.find_element_by_id('question0_question').clear()
        b.find_element_by_id('question0_question').send_keys('Quien esta en primera?')
        b.find_element_by_id('question0_save').click()
        b.find_element_by_xpath('//*[@id="en_tab"]/a').click()

        self._submit_and_check(b)

        new_tab = browser.wait().until(lambda driver: driver.find_element_by_xpath('//*[@id="es_tab"]/a'))
        self.assertEqual(u'Spanish', new_tab.text)

        question = b.find_element_by_xpath('//span[@e-id="question0_question"]')
        b.find_element_by_xpath('//*[@id="es_tab"]/a').click()
        self.assertEqual(question.text, 'Quien esta en primera?')

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

        b.get(self.live_server_url + reverse('brieftemplate_detail', args=[bt.id]))
        self.disable_popups()

        browser.wait().until(lambda driver: driver.find_element_by_id('question_0'))
        with browser.wait_for_page_load():
            b.find_element_by_id('delete_brief').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brieftemplate deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('brieftemplate_detail', args=[bt.id]))
        self.assertEqual(response.status_code, 404)

    def _submit_and_check(self, b):
        with browser.wait_for_page_load():
            b.find_element_by_id('create_submit').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brieftemplate saved.' in success_message.text)
