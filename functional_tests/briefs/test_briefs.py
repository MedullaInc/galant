# coding=utf-8
from django.core.urlresolvers import reverse
from functional_tests import browser
from briefs import models as bm
import autofixture


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
        b.get(self.live_server_url + reverse('brief_list', args=['client', c.id]))
        b.find_element_by_id('add_brief').click()

        # fill out brief & save
        b.find_element_by_name('title').send_keys('Brief test')
        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_edit_client_brief(self):
        b = browser.instance()
        q = autofixture.create_one('briefs.ClientBrief', generate_fk=True)
        q.save()

        b.get(self.live_server_url + reverse('edit_brief', args=['client', q.client.id, q.id]))
        self.load_scripts()

        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_edit_client_brief_question(self):
        b = browser.instance()
        q = bm.Question.objects.create(question='What?')
        mq = bm.MultipleChoiceQuestion.objects.create(question='Huh?', choices=['a', 'b', 'c'], index=1)
        brief = autofixture.create_one('briefs.ClientBrief', generate_fk=True)
        brief.questions.add(q)
        brief.questions.add(mq)

        b.get(self.live_server_url + reverse('edit_brief', args=['client', brief.client.id, brief.id]))
        self.load_scripts()

        b.find_element_by_id('id_title').clear()
        b.find_element_by_id('id_title').send_keys('modified title')

        b.find_element_by_id('id_-question-0-question').send_keys('Who is your daddy, and what does he do?')
        b.find_element_by_id('id_-multiquestion-1-add_choice').click()
        b.find_elements_by_class_name('ultext_array_target')[0].send_keys('foo')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

    def test_add_client_brief_multiquestion(self):
        b = browser.instance()
        q = bm.Question.objects.create(question='What?')
        brief = autofixture.create_one('briefs.ClientBrief', generate_fk=True)
        brief.questions.add(q)

        b.get(self.live_server_url + reverse('edit_brief', args=['client', brief.client.id, brief.id]))
        self.load_scripts()

        b.find_element_by_id('add_multiquestion').click()
        b.find_element_by_id('id_-multiquestion-1-question').send_keys('Who is your daddy, and what does he do?')
        b.find_element_by_id('id_-multiquestion-1-add_choice').click()
        b.find_element_by_id('id_-multiquestion-1-add_choice').click()
        b.find_elements_by_class_name('ultext_array_target')[0].send_keys('foo')
        b.find_elements_by_class_name('ultext_array_target')[1].send_keys('bar')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Brief saved.' in success_message.text)

        answer = b.find_element_by_id('question_1').text
        answer = b.find_element_by_xpath('//div[@id="question_1"]/div/div[1]').text
        self.assertEqual(answer, u'— foo')

    def test_client_brief_detail(self):
        b = browser.instance()
        q = autofixture.create_one('briefs.ClientBrief', generate_fk=True)
        q.save()

        b.get(self.live_server_url + reverse('brief_detail', args=['client', q.client.id, q.id]))
        self.load_scripts()

        section_title = browser.instance().find_element_by_class_name('section_title')
        self.assertEqual(u'Brief Detail', section_title.text)
