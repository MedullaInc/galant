from contextlib import contextmanager

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import selenium.webdriver.support.ui as ui
import autofixture
from django.contrib.auth import hashers
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJS


MAX_TRIES = 3
PAGE_TIMEOUT = 5


class CustomPhantomJS(PhantomJS):
    def get(self, url):
        count = 0

        while True:
            try:
                super(CustomPhantomJS, self).get(url)
                break
            except TimeoutException:
                count += 1
                if count > MAX_TRIES:
                    raise
                else:
                    continue


browser = []


def instance():
    if len(browser) < 1:
        b = CustomPhantomJS(desired_capabilities={'phantomjs.page.settings.resourceTimeout': '5000'})
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

page.onResourceTimeout = function(request) {
  request.abort();
};
''', 'args': []})
        b.set_page_load_timeout(PAGE_TIMEOUT)
        browser.append(b)

    return browser[0]


def close():
    instance().quit()
    browser.pop(0)


def wait(timeout=10):
    return ui.WebDriverWait(instance(), timeout, 0.1)


@contextmanager
def wait_for_page_load(timeout=5):
    b = instance()
    old_page = b.find_element_by_tag_name('html')

    yield

    def page_has_loaded(driver):
        new_page = driver.find_element_by_tag_name('html')
        return new_page.id != old_page.id

    wait(timeout).until(page_has_loaded)


class BrowserTest(StaticLiveServerTestCase):
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

        instance().get(self.live_server_url)
        add_login_cookie(instance(), self.client.session.session_key)

    def tearDown(self):
        instance().delete_all_cookies()


def add_login_cookie(browser_instance, session_key):
    browser_instance.add_cookie({u'domain': u'.localhost', u'name': u'sessionid',
                           u'value': session_key,
                           u'path': u'/', u'httponly': True, u'secure': False})
