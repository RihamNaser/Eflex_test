import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import allure
import logging
import csv


class Eflex_core:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def get_csv_data(csv_path):
        rows = []
        csv_data = open(str(csv_path), "r", encoding="utf8")
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)
        return rows

    def to_activity(self, activity_type):
        actions = ActionChains(self.driver)

        found = False
        while not found:
            current_item = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                '#root > div > div > section > main > div.main-sliders > div > div > div.slick-list > div > div.slick-slide.slick-active.slick-center.slick-current')))
            item_text = current_item.text

            if "SUCCESS LEVEL A2" in item_text:
                found = True
                # time.sleep(6)
            else:
                next_button = self.driver.find_element(By.CSS_SELECTOR,
                                                       '#root > div > div > section > main > div.main-sliders > div > div > div.arrow.right > svg')
                actions.click(next_button).perform()
                self.driver.implicitly_wait(2)

        with allure.step('Select section module'):
            # self.driver.set_window_size(1920, 1080)
            button_element = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div/section/main/div[4]/div[1]/div[2]/span/button')))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button_element)

        if 'text' in activity_type:
            Eflex_core.text_based_Ac(self)
        elif 'image' in activity_type:
            Eflex_core.image_based_Ac(self)
        elif 'audio' in activity_type:
            Eflex_core.audio_based_Ac(self)

    def text_based_Ac(self):
        # WebDriverWait(self.driver, 50).until(
        #     EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, '#root > div > div > section > main > div.main-sliders > div > div')))

        WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div/section/main/div[4]/div[1]/div[2]/span/button'))).click()

        with allure.step('Get the questions and select answers'):
            main_container = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "#root > div > div > section > main > div.module-content > div > div > div > div:nth-child(2) > div.steps-content.first")))

            questions = WebDriverWait(main_container, 50).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "formBuilderField")))

            for question in questions:
                choices = WebDriverWait(question, 50).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio']")))

                for choice in choices:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", choice)
                    self.driver.execute_script("arguments[0].click();", choice)
                    # choice.click()
                    break

        with allure.step('Check answers and get the score'):
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#root > div > div > section > main > div.module-content > div > div > div > div.activity-buttons > div > button:nth-child(1)'))).click()
            score = WebDriverWait(self.driver, 50).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".total-score > p")))[0].text
            allure.attach('\n' + 'Activity score : ' + str(score), "activity_score.text", allure.attachment_type.TEXT)

    def image_based_Ac(self):
        with allure.step('see Image and answer the questions'):
            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/section/main/div[4]/div[3]/div[2]/span/button'))).click()

            image = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "#root > div > div > section > main > div.module-content > div > div > div > div:nth-child(2) > div.steps-content.first > div > div > div > div.activity-question-container > div.ant-row > div.ant-col.ant-col-20 > div > div > div > div > div:nth-child(1) > div:nth-child(1) > div > img")))
            image_loaded = self.driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;",
                                                      image)

            if not image_loaded:
                raise AssertionError("Image is present and visible, but not loaded properly.")

    def audio_based_Ac(self):
        with allure.step('play audio and answer the questions'):
            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/section/main/div[4]/div[3]/div[2]/span/button'))).click()

            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div/section/main/div[2]/aside/div/div[1]/div/div/div[2]'))).click()

            audio_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div > section > main > div.module-content > div > div > div > div.activity-instruction > div.steps-content > div:nth-child(3) > div > div > div > div > audio")))

            audio_playing = self.driver.execute_script("""
                    var audio = arguments[0];
                    return !audio.paused && !audio.ended && audio.currentTime > 0;
                """, audio_element)

            if not audio_playing:
                raise AssertionError("Audio is not playing or is in an invalid state.")

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

    def reach_site(self):
        self.driver.get("https://eflexv2.asal-dev1.eflexlanguages.com/login")

        element = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.ID, "details-button")))
        element.click()

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#proceed-link"))).click()

        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))
