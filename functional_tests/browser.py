from contextlib import contextmanager
import time
from django.test import LiveServerTestCase
from selenium import webdriver
import autofixture
from django.contrib.auth import hashers
from selenium.common.exceptions import NoSuchElementException, WebDriverException

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


def wait_for(condition_function, timeout=3):
    start_time = time.time()
    while time.time() < start_time + timeout:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception('Timeout waiting for {}'.format(condition_function.__name__))


@contextmanager
def wait_for_page_load():
    browser = instance()
    old_page = browser.find_element_by_tag_name('html')

    yield

    def page_has_loaded():
        new_page = browser.find_element_by_tag_name('html')
        return new_page.id != old_page.id

    wait_for(page_has_loaded)


def wait_for_element(search_function, *args):
    def element_exists():
        try:
            search_function(*args)
        except NoSuchElementException:
            return False

        return True

    wait_for(element_exists)


class BrowserTest(LiveServerTestCase):
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
