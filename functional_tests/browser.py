from django.test import LiveServerTestCase
from selenium import webdriver
import autofixture
from django.contrib.auth import hashers


browser = []


def instance():
    if len(browser) < 1:
        b = webdriver.PhantomJS()
        # hack while the python interface lags
        b.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')

        b.execute('executePhantomScript', {'script': '''
    var page = this; // won't work otherwise
    page.onResourceRequested = function(requestData, request) {
        if ((/http:\/\/.+?\.css/gi).test(requestData['url']) || requestData['Content-Type'] == 'text/css') {
            console.log('The url of the request is matching. Aborting: ' + requestData['url']);
            request.abort();
        }
}
''', 'args': []})
        browser.append(b)
    return browser[0]


def close():
    instance().quit()
    browser.pop(0)


class BrowserTest(LiveServerTestCase):
    def load_scripts(self):
        '''
        Call this method after loading target page to load jQuery and scripts contained
        within <body> (Selenium doesn't automatically load them).
        :return:
        '''
        b = instance()
        scripts = b.find_elements_by_xpath('//script')
        for s in scripts:
            js = s.get_attribute('innerHTML')
            if len(js) > 0:
                b.execute_script(js)

    def disable_popups(self):
        '''
        Call this method to disable alerts and popups.
        :return:
        '''
        b = instance()

        # need this to auto-accept all confirmation dialogs
        b.execute_script("window.confirm = function(){return true;}")
        b.execute_script("window.alert = function(){}")
        b.execute_script("window.onbeforeunload = function(){}")

    def save_snapshot(self):  # pragma: no cover
        b = instance()
        b.save_screenshot('test_out.png')
        import codecs
        with codecs.open('test_out.html', 'w+', 'utf8') as f:
            f.write(b.page_source)

        with open('test_out.txt', 'w+') as f:
            for entry in b.get_log('browser'):
                f.write(str(entry) + '\n')


class SignedInTest(BrowserTest):
    def setUp(self):
        self.user = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                           field_values={'password': hashers.make_password('password')})
        self.user.save()

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # add session cookie for logged-in user
        self.client.login(email=self.user.email, password='password')
        instance().add_cookie({u'domain': u'localhost', u'name': u'sessionid',
                               u'value': self.client.session.session_key,
                               u'path': u'/', u'httponly': True, u'secure': False})

    def tearDown(self):
        instance().delete_all_cookies()
