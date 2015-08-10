from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser
from selenium.common.exceptions import NoSuchElementException


def tearDown():
    browser.close()


class GallantAccountTest(browser.SignedInTest):
    pass

