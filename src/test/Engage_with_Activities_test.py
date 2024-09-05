import unittest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from ddt import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
csv_path = os.path.join(os.path.dirname(__file__), '../config/activities_types.csv')
from core.Constants import Constants
from core.login_page import LoginPage
from core.Eflex_core import Eflex_core


@ddt
class Activities_Completeness_test(unittest.TestCase):

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

    @data(*Eflex_core.get_csv_data(csv_path))
    @unpack
    def test_Complete_Activities(self, activity_type):
        allure.dynamic.title(f"Test Ensuring User Can Engage with an {activity_type}")

        login_page = LoginPage(self.driver)
        Eflex_activity = Eflex_core(self.driver)
        Eflex_activity.reach_site()

        self.driver.get(self.path)

        with allure.step('Log in to Learner page'):
            login_page.log_in(Constants.username, Constants.password)

            allure.attach(
                '\n' + 'The username used in the test : ' + str(Constants.username) + '\n' +
                '\n' + 'The password used in the test : ' + str(Constants.password), "test_credentials.text",
                allure.attachment_type.TEXT)

        with allure.step('Activity check'):
            Eflex_activity.to_activity(activity_type)


if __name__ == '__main__':
    unittest.main()
