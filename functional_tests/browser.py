from contextlib import contextmanager

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import selenium.webdriver.support.ui as ui
import autofixture
from django.contrib.auth import hashers
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJS

from django.core.servers import basehttp
from wsgiref.simple_server import WSGIServer as base_wsgi


def my_handle_error(self, request, client_address):
    if not basehttp.is_broken_pipe_error():
        base_wsgi.handle_error(self, request, client_address)
basehttp.WSGIServer.handle_error = my_handle_error


MAX_TRIES = 3
PAGE_TIMEOUT = 7
SNAP_PREFIX = 'test_out'


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


def save_driver_snapshot(driver, prefix=SNAP_PREFIX):
    driver.save_screenshot('%s.png' % prefix)
    import codecs
    with codecs.open('%s.html' % prefix, 'w+', 'utf8') as f:
        f.write(driver.page_source)

    with open('%s.txt' % prefix, 'w+') as f:
        for entry in driver.get_log('browser'):
            f.write(str(entry) + '\n')


class CustomWait(ui.WebDriverWait):
    def __init__(self, *args, **kwargs):
        super(CustomWait, self).__init__(*args, **kwargs)
        iex = list(self._ignored_exceptions)
        iex.append(StaleElementReferenceException)
        iex.append(ElementNotVisibleException)
        self._ignored_exceptions = tuple(iex)

    def until(self, method, message=''):
        try:
            return super(CustomWait, self).until(method, message)
        except TimeoutException, ex:
            save_driver_snapshot(self._driver)
            raise type(ex)(ex.message + 'Wait timed out. Driver snapshot saved to %s.png/txt/html' % SNAP_PREFIX)

    def until_click(self, method, message=''):
        try:
            return super(CustomWait, self).until(lambda x: self.until(method).click() is None, message)
        except TimeoutException, ex:
            save_driver_snapshot(self._driver)
            raise type(ex)(ex.message + 'Wait timed out. Driver snapshot saved to %s.png/txt/html' % SNAP_PREFIX)


def custom_phantomjs():
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
    return b


browser = []


def instance():
    if len(browser) < 1:
        b = custom_phantomjs()
        browser.append(b)

    return browser[0]


def close():
    instance().quit()
    browser.pop(0)


def wait(timeout=10):
    return CustomWait(instance(), timeout, 0.1)


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

    def disable_angular_popups(self, b):
        b.execute_script('''
            var elem = angular.element(document.querySelector('[ng-controller]'));
            var injector = elem.injector();
            var w = injector.get('$window');

            w.confirm = function() { return true; };
            w.alert = function() {};
            w.onbeforeunload = function() {};
            elem.scope().$apply();
        ''')


    def save_snapshot(self, prefix=SNAP_PREFIX):  # pragma: no cover
        save_driver_snapshot(instance(), prefix)


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

    def create_one(self, cls, field_values={}):
        field_values.update({'user': self.user})
        autofixture.create_one(cls, generate_fk=True, field_values=field_values)


def add_login_cookie(browser_instance, session_key):
    browser_instance.add_cookie({u'domain': u'.localhost', u'name': u'sessionid',
                           u'value': session_key,
                           u'path': u'/', u'httponly': True, u'secure': False})
