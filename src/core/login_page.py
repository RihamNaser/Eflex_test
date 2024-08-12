from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, 'username')
        self.password_input = (By.ID, 'password')
        self.login_button = (By.ID, 'signinBtn')

    def enter_username(self, username):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.username_input)).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.password_input)).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.login_button)).click()

    def log_in(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
