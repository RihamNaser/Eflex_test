import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class Eflex_core:
    def __init__(self, driver):
        self.driver = driver

    def to_activity(self):
        with allure.step('Select section module'):
            self.driver.set_window_size(1920, 1080)
            button_element = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/main/div[4]/div[1]/div[2]/span/button')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button_element)

            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/section/main/div[4]/div[1]/div[2]/span/button'))).click()

        with allure.step('Get the questions and select answers'):
            main_container = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div > section > main > div.module-content > div > div > div > div:nth-child(2) > div.steps-content.first")))
            # main_container = self.driver.find_element(By.CSS_SELECTOR, "#root > div > div > section > main > div.module-content > div > div > div > div:nth-child(2) > div.steps-content.first")
            # questions = main_container.find_elements(By.CLASS_NAME, "formBuilderField")
            questions = WebDriverWait(main_container, 50).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "formBuilderField")))

            for question in questions:
                choices = WebDriverWait(question, 50).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio']")))

                for choice in choices:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", choice)
                    time.sleep(5)
                    self.driver.execute_script("arguments[0].click();", choice)
                    # choice.click()
                    break

        with allure.step('Check answers and get the score'):
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div > section > main > div.module-content > div > div > div > div.activity-buttons > div > button:nth-child(1)'))).click()
            time.sleep(5)
            score = self.driver.find_element(By.CSS_SELECTOR, "div.activity-score div.total-score p").text

        return score

    def content_type(self):
        images = self.driver.find_elements(By.TAG_NAME, "img")
        videos = self.driver.find_elements(By.TAG_NAME, "video")
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        audios = self.driver.find_elements(By.TAG_NAME, "audio")

        if images:
            return "Image"
        if videos or iframes:
            return "Video"
        if audios:
            return "Audio"
        else:
            return "Text"
