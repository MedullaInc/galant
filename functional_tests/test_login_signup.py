from functional_tests import browser


class LoginSignUpTest(browser.SignedInTest):
    def setUp(self):
        super(LoginSignUpTest, self).setUp()
        browser.get().get(self.live_server_url)

    def test_cant_login(self):
        body = browser.get().find_element_by_tag_name('body')
        self.assertNotIn('Account Login', body.text)

    def test_cant_sign_up(self):
        body = browser.get().find_element_by_tag_name('body')
        self.assertNotIn('Sign Up Now!', body.text)

    def test_can_sign_out(self):
        body = browser.get().find_element_by_tag_name('body')
        self.assertIn('Sign Out', body.text)

