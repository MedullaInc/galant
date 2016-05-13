from functional_tests import browser


def tearDownModule():
    browser.close()


class AdminTest(browser.SignedInTest):
    def test_can_access_admin_site(self):
        self.get(self.live_server_url + '/en/admin/')
        # check 'Django administration' heading
        body = self.e_tag('body')
        self.assertIn('Django administration', body.text)

