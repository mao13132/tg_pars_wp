import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class WpAddPost:
    def __init__(self, driver, BotDB, site_data):
        self.driver = driver
        self.source_name = 'WP'
        self.BotDB = BotDB
        self.site_data = site_data

    def write_text_in_frame(self, value):
        try:
            _frame = self.driver.find_element(by=By.XPATH,
                                              value=f"//*[contains(@id, 'wp-content')]//iframe")
        except:
            return False

        self.driver.switch_to.frame(_frame)
        try:
            insert_element = self.driver.find_element(by=By.XPATH,
                                                      value=f"//body[contains(@id, 'tinymce')]/p")
        except:
            self.driver.switch_to.default_content()
            return False

        try:
            insert_element.send_keys('\n')
            time.sleep(1)
        except:
            pass

        try:
            self.driver.execute_script(
                f'''
                        const text = `{value}`;
                        const dataTransfer = new DataTransfer();
                        dataTransfer.setData('text', text);
                        const event = new ClipboardEvent('paste', {{
                          clipboardData: dataTransfer,
                          bubbles: true
                        }});
                        arguments[0].dispatchEvent(event)
                        ''',
                insert_element)
        except Exception as es:
            print(f"Не смог вписать сообщение '{es}'")
            return False

        self.driver.switch_to.default_content()

        return True

    def click_add_media_button(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@id, 'wp-content')]"
                                           f"//button[contains(@class, 'insert-media')]").click()

        except:
            return False

        return True

    def click_add_media_preview(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@id, 'postimagediv')]//a").click()

        except:
            return False

        return True

    def click_button_insert(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'media-button-insert')]").click()

        except:
            return False

        return True

    def click_button_preview(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'media-button-select')]").click()

        except:
            return False

        return True

    def check_load_modal_image(self):
        count = 0
        count_try = 15

        while True:
            count += 1
            if count > count_try:
                print(f'Не смог открыть окно для загрузки медиафайлов')
                return False

            try:
                status = self.driver.find_element(by=By.XPATH,
                                                  value=f"//*[contains(@class, 'supports-drag-drop')]").get_attribute(
                    'style')
            except:
                time.sleep(1)
                continue

            if 'none' in status:
                time.sleep(1)
                continue

            return True

    def check_load_modal_preview(self):
        count = 0
        count_try = 15

        while True:
            count += 1
            if count > count_try:
                print(f'Не смог открыть окно для загрузки медиафайлов')
                return False

            try:
                status = self.driver.find_elements(by=By.XPATH,
                                                   value=f"//*[contains(@class, 'supports-drag-drop')]")[
                    -1].get_attribute(
                    'style')
            except:
                time.sleep(1)
                continue

            if 'none' in status:
                time.sleep(1)
                continue

            return True

    def _insert_image(self, images_list):

        for img in images_list:
            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f"//input[contains(@id, 'html5_')]").send_keys(img)
            except:
                continue

        return True

    def check_full_load(self):
        count = 0
        while True:
            count += 1
            if count > 60:
                return False

            try:
                self.driver.find_element(by=By.XPATH, value=f"//button[contains(@disabled, 'disabled')]")
                time.sleep(1)
            except:
                return True

    def click_publish(self):
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//div[@id='submitdiv']//*[@id='publishing-action']//*[@name='publish']")
            ActionChains(self.driver).move_to_element(el).perform()
        except:
            pass

        try:
            self.driver.find_element(by=By.XPATH, value=f"//div[@id='submitdiv']"
                                                        f"//*[@id='publishing-action']//*[@name='publish']").click()
            # self.driver.find_element(by=By.XPATH, value=f"//*[@id='publish']").click()
        except:
            return False

        try:
            alert_obj = self.driver.switch_to.alert
            alert_obj.accept()
            self.driver.switch_to.default_content()
        except:
            pass

        return True

    def wait_load_media(self):
        try:
            time.sleep(10)
            self.driver.find_element(by=By.XPATH,
                                     value=f"//input[contains(@id, 'html5_')]").send_keys(Keys.ESCAPE)
            time.sleep(3)
        except:
            return False

        return True

    def click_category(self, value):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'taxonomy-category')]"
                                                        f"//*[contains(text(), '{value}')]").click()
            print(f'Установил категорию "{value}"')
        except:
            return False

        return True

    def formated_title(self, value):
        msg = ''
        for x in value:
            if x.isalpha():
                msg += x
            else:
                if x == ' ':
                    msg += x

        return msg


    def write_title(self, text):
        try:
            _text = text.split('\n')[0]
        except:
            _text = text[:10]

        _text = self.formated_title(_text)

        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[@name='post_title']").send_keys(_text)
        except:
            return False



        return True

    def insert_image_universal(self, images_list):

        res_add_images = self.click_add_media_button()

        self.check_load_modal_image()

        res_insert = self._insert_image(images_list)

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button_insert()

        return True

    def click_load_more(self):
        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=f"//*[contains(text(), 'Загрузить файлы')]")[-1].click()
        except:
            return False

        return True

    def insert_image_preview(self, images_list):

        res_add_images = self.click_add_media_preview()

        self.check_load_modal_preview()

        res_add_images = self.click_load_more()

        res_insert = self._insert_image([images_list])

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button_preview()

        return True

    def check_publish(self):
        count = 0
        count_try = 60
        while True:
            count += 1
            if count > count_try:
                print(f'Не могу подтвердить публикацию записи')
                return False

            try:
                self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Запись опубликована')]")

                return True
            except:
                time.sleep(1)
                continue
