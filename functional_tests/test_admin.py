from functional_tests.test_signed_in import SignedInTest, get_browser, quit_browser


def teardown():
    quit_browser()


class AdminTest(SignedInTest):
    def test_can_access_admin_site(self):
        b = get_browser()
        b.get(self.live_server_url + '/admin/')
        # check 'Django administration' heading
        body = b.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

