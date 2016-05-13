from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm


def tearDownModule():
    browser.close()


class BriefTemplatesTest(browser.SignedInTest):
    def setUp(self):
        super(BriefTemplatesTest, self).setUp()
        self.brief = self.create_one('briefs.Brief')
        self.bt = self.create_one('briefs.BriefTemplate', {'brief': self.brief})
        self.disable_popups()

    def test_add_brief_template(self):
        self.get(self.live_server_url + reverse('add_brief_template'))

        self.click_id('brief_save')
        self.e_id('brief_title').send_keys('Brief test')
        self.e_id('brief_greeting').send_keys('Brief test')

        self._submit_and_check(True)

    def test_brieftemplate_detail(self):
        self.get(self.live_server_url + reverse('brieftemplate_detail', args=[self.bt.id]))

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Brief Template Detail', app_title.text)

    def test_add_brief_lang_dropdown(self):
        self.get(self.live_server_url + reverse('add_brief_template'))

        self.click_id('brief_save')
        self.e_id('brief_title').send_keys('Brief test')
        self.e_id('brief_greeting').send_keys('Brief test')

        self._add_language_and_text(True)

    def test_brief_edit_template(self):
        q = bm.TextQuestion.objects.create(user=self.brief.user, question='What?')
        self.brief.questions.add(q)
        self.get(self.live_server_url + reverse('brieftemplate_detail', args=[self.bt.id]))

        self.click_id('brief_edit')
        self.e_id('question0_question').clear()
        self.e_id('question0_question').send_keys('modified question')

        self._submit_and_check()

        quest = self.e_xpath('//p[@e-id="question0_question"]')
        self.assertEqual(quest.text, 'modified question')

    def test_brief_edit_lang_dropdown(self):
        self.get(self.live_server_url + reverse('brieftemplate_detail', args=[self.bt.id]))

        browser.wait().until(lambda driver: driver.find_element_by_xpath('//h2[@e-id="brief_title"]').text != 'Not set')
        self._add_language_and_text()

    def test_add_from_brief(self):
        quest = bm.TextQuestion.objects.create(user=self.brief.user)
        self.brief.questions.add(quest)
        self.get(self.live_server_url + reverse('add_brief_template') + '?brief_id=%d' % self.brief.id)

        question = self.e_xpath('//p[@e-id="question0_question"]')
        self.assertEqual('Not set', question.text)

    def test_add_brief_from_template(self):
        quest = bm.TextQuestion.objects.create(user=self.brief.user, question='Who\'s on first?')
        self.brief.questions.add(quest)
        self.brief.client = self.create_one('gallant.Client')
        self.brief.save()
        self.get(self.live_server_url +
              reverse('add_brief') + '?template_id=%d&lang=en&client_id=%d' % (self.bt.id, self.brief.client.id))

        browser.wait().until(lambda driver: driver.find_element_by_id('question0'))
        question = self.e_xpath('//p[@e-id="question0_question"]')
        self.assertEqual(quest.question.get_text(), question.text)

        with browser.wait_for_page_load():
            self.e_id('brief_save').click()

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def _add_language_and_text(self, redirect=False):
        self.e_id('add_question').click()
        self.e_id('question0_question').clear()
        self.e_id('question0_question').send_keys('Who\'s on first?')
        self.e_id('add_translation_button').click()
        self.e_xpath('//select[@id="id_language"]/option[text()[1]="Spanish"]').click()
        self.e_id('language_add').click()
        self.e_xpath('//*[@id="es_tab"]/a').click()
        self.e_id('brief_title').send_keys('Brief prueba')
        self.e_id('brief_greeting').send_keys('Brief prueba')
        self.e_id('question0_question').clear()
        self.e_id('question0_question').send_keys('Quien esta en primera?')

        self._submit_and_check(redirect)

        new_tab = browser.wait().until(lambda driver: driver.find_element_by_xpath('//*[@id="es_tab"]/a'))
        self.assertEqual(u'Spanish', new_tab.text)

        question = self.e_xpath('//p[@e-id="question0_question"]')
        self.e_xpath('//*[@id="es_tab"]/a').click()
        self.assertEqual(question.text, 'Quien esta en primera?')

    def test_can_access_brief_template_endpoint(self):
        response = self.client.get(self.live_server_url + reverse('api-brief-template-detail', args=[self.bt.id]))
        self.assertEqual(response.status_code, 200)

    def test_soft_delete_brief_template(self):
        self.brief.status = '0'
        self.brief.save()
        q = bm.TextQuestion.objects.create(user=self.brief.user, question='What?')
        self.brief.questions.add(q)

        self.get(self.live_server_url + reverse('brieftemplate_detail', args=[self.bt.id]))

        self.e_id('question_0')
        self.disable_popups()
        self.disable_angular_popups()

        self.submit('brief_delete')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Brieftemplate deleted.' in success_message.text)

        # check that brief access returns 404
        response = self.client.get(self.live_server_url + reverse('brieftemplate_detail', args=[self.bt.id]))
        self.assertEqual(response.status_code, 404)

    def _submit_and_check(self, redirect=False):
        if redirect:
            self.submit('brief_save')
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Brieftemplate saved.' in success_message.text)
        else:
            self.e_id('brief_save').click()
            success_message = self.e_class('alert-success')
            self.assertTrue(u'Saved.' in success_message.text)
