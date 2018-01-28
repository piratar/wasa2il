import unittest
from selenium import webdriver

browser = webdriver.Firefox()

# If needed, download geckodriver here: https://github.com/mozilla/geckodriver/releases
# And add it to /usr/local/bin/

class TestSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_verify_frontpage(self):
        self.driver.get("http://localhost:8000/")
        assert "Voting System" in self.driver.title
        self.driver.find_element_by_id('wrapper')
        self.driver.find_element_by_id('sidebar-wrapper')
        self.driver.find_element_by_id('issues-recent')
        self.driver.find_element_by_id('elections-recent')

    def test_signup_fire(self):
        self.driver.get("http://localhost:8000/accounts/register")
        self.driver.find_element_by_id('id_username').send_keys("testuser")
        self.driver.find_element_by_id('id_email').send_keys("testuser@example.com")
        self.driver.find_element_by_id('id_password1').send_keys("testuser")
        self.driver.find_element_by_id('id_password2').send_keys("testuser")
        #self.driver.find_element_by_id('submit').click()
        self.driver.find_element_by_class_name('btn-primary').click()

        #self.driver.get("http://localhost:8000/")
        #self.driver.find_element_by_id('id_title').send_keys("test title")
        #self.driver.find_element_by_id('id_body').send_keys("test body")
        #self.driver.find_element_by_id('submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def test_can_login(self):
        self.driver.get("http://localhost:8000/accounts/login")
        self.driver.find_element_by_id('id_username').send_keys("testuser")
        self.driver.find_element_by_id('id_password').send_keys("testuser")
        self.driver.find_element_by_class_name('btn-primary').click()

        # Verify we find this warning on the page: 'This account is inactive.'
        self.driver.find_element_by_class_name('alert-danger')
        # Email needs to be verified

    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()
