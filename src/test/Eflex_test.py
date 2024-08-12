import unittest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from core.Constants import Constants
from core.login_page import LoginPage
from core.Eflex_core import Eflex_core


class Eflex_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = Service()
        cls.chrome_options = webdriver.ChromeOptions()
        cls.path = Constants.path
        # cls.chrome_options.add_argument('--headless')

    def setUp(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

    def tearDown(self):
        self.driver.quit()

    def test_Eflex(self):
        login_page = LoginPage(self.driver)
        Eflex_activity = Eflex_core(self.driver)

        self.driver.get(self.path)
        with allure.step('Log in to Learner page'):
            login_page.log_in(Constants.username, Constants.password)
        with allure.step('Activity check'):
            score = Eflex_activity.to_activity()
            print(score)


if __name__ == '__main__':
    unittest.main()
