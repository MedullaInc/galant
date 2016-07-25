from functional_tests import browser


def tearDownModule():
    browser.close()


class LoginSignUpTest(browser.SignedInTest):
    def setUp(self):
        super(LoginSignUpTest, self).setUp()
        self.get(self.live_server_url+'/en/')

    def test_cant_login(self):
        body = self.e_tag('body')
        self.assertNotIn('Account Login', body.text)

    def test_cant_sign_up(self):
        body = self.e_tag('body')
        self.assertNotIn('Sign Up Now!', body.text)

    def test_can_sign_out(self):
        body = self.e_tag('body')
        self.assertIn('Log Out', body.text)

