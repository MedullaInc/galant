from django.test import LiveServerTestCase
from selenium import webdriver
import autofixture
from django.contrib.auth import hashers


browser = []


def instance():
    if len(browser) < 1:
        browser.append(webdriver.PhantomJS())
    return browser[0]


def close():
    instance().quit()
    browser.pop(0)


class SignedInTest(LiveServerTestCase):
    def setUp(self):
        u = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                   field_values={'password': hashers.make_password('password')})
        u.save()

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # add session cookie for logged-in user
        self.client.login(email=u.email, password='password')
        instance().add_cookie({u'domain': u'localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

    def tearDown(self):
        instance().delete_all_cookies()

    def load_scripts(self):
        '''
        Call this method after loading target page to load jQuery and scripts contained
        within <body> (Selenium doesn't automatically load them).
        :return:
        '''
        b = instance()
        with open("static/js/jquery-latest.min.js", "r") as jq:
            b.execute_script(jq.read())
        with open("static/js/bootstrap.min.js", "r") as jq:
            b.execute_script(jq.read())
        with open("static/js/gallant.js", "r") as jq:
            b.execute_script(jq.read())

        scripts = b.find_elements_by_xpath('//body/script')
        for s in scripts:
            b.execute_script(s.get_attribute('innerHTML'))

        # need this to auto-accept all confirmation dialogs
        b.execute_script("window.confirm = function(){return true;}")
        b.execute_script("window.alert = function(){}")

