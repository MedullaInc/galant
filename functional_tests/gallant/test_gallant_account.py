from django.contrib.auth import hashers, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
import autofixture
from functional_tests import browser


def tearDownModule():
    browser.close()


class GallantAccountTest(browser.BrowserTest):
    def test_add_account(self):
        Group.objects.get_or_create(name='users')  # not in the DB sometimes for some unknown reason

        user = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                      field_values={'password': hashers.make_password('password'),
                                                    'is_superuser': True})
        user.save()
        self.client.login(email=user.email, password='password')

        browser.add_login_cookie(self.b, self.client.session.session_key)

        self.get(self.live_server_url + reverse('add_account'))

        self.e_name('email').send_keys('foo@bar.com')

        self.click_xpath('//button[@type="submit"]')

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Registration link sent.' in success_message.text)

    def test_reset_password(self):
        autofixture.create_one('gallant.GallantUser', generate_fk=True,
                               field_values={'email': 'foo@bar.com'})

        user = autofixture.create_one('gallant.GallantUser', generate_fk=True,
                                      field_values={'password': hashers.make_password('password'),
                                                    'is_superuser': True})
        user.save()
        self.client.login(email=user.email, password='password')
        browser.add_login_cookie(self.b, self.client.session.session_key)

        self.get(self.live_server_url + reverse('reset_password'))

        self.e_name('email').send_keys('foo@bar.com')

        self.e_xpath('//button[@type="submit"]').click()

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Password reset link sent.' in success_message.text)

    def test_register(self):

        UserModel = get_user_model()
        user = UserModel.objects.create(email='foo@bar.com')
        token = default_token_generator.make_token(user)

        self.get(self.live_server_url + reverse('register', args=[user.id]) + '?token=%s' % token)

        self.e_name('new_password1').send_keys('12344321')
        self.e_name('new_password2').send_keys('12344321')

        self.e_name('name').send_keys('foo bar')
        self.e_name('company_name').send_keys('foo inc.')

        self.e_name('phone_number').send_keys('5281833666666')  # error here, digits are entered wrong
        self.e_name('address').send_keys('asdf')
        self.e_name('city').send_keys('asdf')
        self.e_name('state').send_keys('asdf')
        self.e_name('zip').send_keys('12345')

        self.e_xpath('//button[@type="submit"]').click()

        success_message = self.e_class('alert-success')
        self.assertTrue(u'Registration successful.' in success_message.text)

    def test_register_invalid(self):

        UserModel = get_user_model()
        user = UserModel.objects.create(email='foo@bar.com')
        token = default_token_generator.make_token(user)

        self.get(self.live_server_url + reverse('register', args=[user.id]) + '?token=%s' % token)

        self.click_xpath('//button[@type="submit"]')

        app_title = self.e_class('app_title')
        self.assertEqual('Register', app_title.text)
