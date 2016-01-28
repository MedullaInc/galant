from django.contrib.auth import hashers, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDown():
    browser.close()


def teardown_module(module):
    browser.close()


class GallantAccountTest(StaticLiveServerTestCase):
    def test_add_account(self):
        b = browser.instance()
        Group.objects.get_or_create(name='users')  # not in the DB sometimes for some unknown reason

        user = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                      field_values={'password': hashers.make_password('password'),
                                                    'is_superuser': True})
        user.save()
        self.client.login(email=user.email, password='password')

        b.add_cookie({u'domain': u'.localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

        b.get(self.live_server_url + reverse('add_account'))

        b.find_element_by_name('email').send_keys('foo@bar.com')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Registration link sent.' in success_message.text)

    def test_reset_password(self):
        b = browser.instance()
        autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                      field_values={'email': 'foo@bar.com'})

        user = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                      field_values={'password': hashers.make_password('password'),
                                                    'is_superuser': True})
        user.save()
        self.client.login(email=user.email, password='password')
        b.add_cookie({u'domain': u'.localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

        b.get(self.live_server_url + reverse('reset_password'))

        b.find_element_by_name('email').send_keys('foo@bar.com')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Password reset link sent.' in success_message.text)

    def test_register(self):
        b = browser.instance()

        UserModel = get_user_model()
        user = UserModel.objects.create(email='foo@bar.com')
        token = default_token_generator.make_token(user)

        b.get(self.live_server_url + reverse('register', args=[user.id]) + '?token=%s' % token)

        b.find_element_by_name('new_password1').send_keys('12344321')
        b.find_element_by_name('new_password2').send_keys('12344321')

        b.find_element_by_name('name').send_keys('foo bar')
        b.find_element_by_name('company_name').send_keys('foo inc.')

        b.find_element_by_name('contact_info.phone_number').send_keys('5281833666666')  # error here, digits are entered wrong
        b.find_element_by_name('contact_info.address').send_keys('asdf')
        b.find_element_by_name('contact_info.city').send_keys('asdf')
        b.find_element_by_name('contact_info.state').send_keys('asdf')
        b.find_element_by_name('contact_info.zip').send_keys('12345')

        b.find_element_by_xpath('//button[@type="submit"]').click()

        success_message = b.find_element_by_class_name('alert-success')
        self.assertTrue(u'Registration successful.' in success_message.text)

    def test_register_invalid(self):
        b = browser.instance()

        UserModel = get_user_model()
        user = UserModel.objects.create(email='foo@bar.com')
        token = default_token_generator.make_token(user)

        b.get(self.live_server_url + reverse('register', args=[user.id]) + '?token=%s' % token)

        b.find_element_by_xpath('//button[@type="submit"]').click()

        app_title = browser.instance().find_element_by_class_name('app_title')
        self.assertEqual('Register', app_title.text)
