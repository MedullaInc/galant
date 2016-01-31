from functional_tests import browser


def tearDownModule():
    browser.close()


class AdminTest(browser.SignedInTest):
    def test_can_access_admin_site(self):
        b = browser.instance()
        b.get(self.live_server_url + '/en/admin/')
        # check 'Django administration' heading
        body = b.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

