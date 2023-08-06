import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

from telegram_debug import SendlerOneCreate


class WpAddPost:
    def __init__(self, driver, BotDB, site_data):
        self.driver = driver
        self.source_name = 'WP'
        self.BotDB = BotDB
        self.site_data = site_data

    def write_text_in_frame(self, value):
        one_version = True
        try:
            _frame = self.driver.find_element(by=By.XPATH,
                                              value=f"//*[contains(@id, 'wp-content')]//iframe")
            ActionChains(self.driver).move_to_element(_frame).perform()
        except:
            try:
                one_version = False
                insert_element = self.driver.find_element(by=By.XPATH,
                                                          value=f"//*[contains(@id, 'wp-content')]//textarea")
            except:
                return False

        if one_version:

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

        if one_version:
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
        else:
            self.driver.execute_script("""
              var elm = arguments[0], txt = arguments[1];
              elm.value += txt;
              elm.dispatchEvent(new Event('change'));
              """, insert_element, value)

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
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//*[@id='postimagediv']//a")
            # value=f"//*[contains(@id, 'postimagediv')]//a").click()

        except:
            return False

        ActionChains(self.driver).move_to_element(el).perform()

        try:
            el.click()

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

    def check_close(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@id, 'submitdiv') and contains(@class, 'closed')]"
                                           f"//*[@id='publishing-action']//input[@name='publish']")
        except:
            return False

        return True

    def open_tulbar_publish(self):
        try:
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//div[contains(@id, 'submitdiv') and contains(@class, 'closed')]"
                                                f"//*[contains(text(), 'Опубликовать')]")
        except:
            return False

        try:
            ActionChains(self.driver).move_to_element(el).perform()
        except:
            return False

        try:
            el.click()
        except:
            return False

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

    def check_close_category(self):
        try:
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//div[contains(@id, 'categorydiv') and contains(@class, 'closed')]")
            ActionChains(self.driver).move_to_element(el).perform()
        except:
            return False

        return True

    def open_close_category(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@id, 'categorydiv') "
                                           f"and contains(@class, 'closed')]").click()
        except:
            return False

        return True

    def click_category(self, value):
        try:
            el = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'taxonomy-category')]"
                                                             f"//*[contains(text(), '{value}')]")

        except:
            return False

        ActionChains(self.driver).move_to_element(el).perform()

        try:
            el.click()
        except:
            return False

        return True

    def job_category(self, value):
        status_category = self.check_close_category()

        if status_category:
            self.open_close_category()

        SendlerOneCreate(self.driver).send_error_tg_img(f'Проверка категории')

        res_set_category = self.click_category(value)

        return res_set_category

    def formated_title(self, value):
        msg = ''
        for x in value:
            if x.isalpha():
                msg += x
            else:
                if x == ' ':
                    msg += x

        return msg

    def check_modal_popup(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@role, 'document')]"
                                                        f"//*[contains(@type, 'button')]").click()
        except:
            return False

        return True

    def write_title(self, text):
        try:
            _text = text.split('\n')[0]
        except:
            _text = 'Новость'

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

    def check_close_preview(self):
        try:
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//div[contains(@id, 'postimagediv') and contains(@class, 'closed')]")
            ActionChains(self.driver).move_to_element(el).perform()
        except:
            return False

        return True

    def open_close_preview(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//div[contains(@id, 'postimagediv') "
                                           f"and contains(@class, 'closed')]").click()
        except:
            return False

        return True

    def insert_image_preview(self, images_list):

        status_close = self.check_close_preview()

        if status_close:
            self.open_close_preview()

        res_add_images = self.click_add_media_preview()

        self.check_load_modal_preview()

        res_add_images = self.click_load_more()

        res_insert = self._insert_image([images_list])

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button_preview()

        return True

    def check_load_preview(self):
        try:
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//*[contains(text(), "
                                                f"'Нажмите на изображение, чтобы изменить или обновить его')]")
        except:
            return False

        return True

    def loop_set_preview(self, images_list):
        count = 0
        count_try = 5
        while True:
            count += 1

            if count > count_try:
                print(f'Не смог выставить изображение на превью')
                SendlerOneCreate(self.driver).send_error_tg_img(f'')
                return False

            res_load = self.check_load_preview()

            if not res_load:
                self.insert_image_preview(images_list)
                if count > 1:
                    time.sleep(1)

                continue

            # SendlerOneCreate(self.driver).send_error_tg_img(f'')

            return True

    def click_publish(self):
        from telegram_debug import SendlerOneCreate
        # SendlerOneCreate(self.driver).send_error_tg_img(f'Начинаю опубликовывать')
        status_close = self.check_close()

        if status_close:
            self.open_tulbar_publish()

        try:
            el = self.driver.find_element(by=By.XPATH,
                                          value=f"//div[@id='submitdiv']"
                                                f"//*[@id='publishing-action']//*[@name='publish']")

            ActionChains(self.driver).move_to_element(el).perform()

        except:
            return False

        try:
            # self.driver.find_element(by=By.XPATH, value=f"//div[@id='submitdiv']"
            #                                             f"//*[@id='publishing-action']//*[@name='publish']").click()
            el.click()
        except:
            return False

        try:
            alert_obj = self.driver.switch_to.alert
            alert_obj.accept()
            self.driver.switch_to.default_content()
        except:
            pass

        SendlerOneCreate(self.driver).send_error_tg_img(f'')

        return True

    def check_publish(self):
        count = 0
        count_try = 20
        while True:
            count += 1
            if count > count_try:
                return False

            try:
                self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Запись опубликована')]")

                return True
            except:
                try:
                    self.driver.find_element(by=By.XPATH,
                                             value=f"//div[contains(@id, 'submitdiv')]"
                                                   f"//input[contains(@value, 'Обновить')]")

                    return True
                except:
                    time.sleep(3)
                    continue

    def loop_publish(self):
        res_click = self.click_publish()

        res_publish = self.check_publish()

        return res_publish
