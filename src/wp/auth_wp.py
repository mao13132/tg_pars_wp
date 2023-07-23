import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthWP:
    def __init__(self, driver, site_link, login, password):
        self.driver = driver
        self.source_name = site_link
        self.login = login
        self.password = password

    def write_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'user_login')]").send_keys(self.login)
        except Exception as es:
            print(f'Не смог ввести логин "{es}"')
            return False

    def write_password(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'user_pass')]").send_keys(self.password)
        except Exception as es:
            print(f'Не смог ввести пароль "{es}"')
            return False

    def check_email(self):
        try:
            email = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'user_login')]").get_attribute(
                'value')
        except Exception as es:
            print(f'Не смог проверить email "{es}"')
            return False

        return email

    def check_password(self):
        try:
            password_ = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'user_pass')]").get_attribute(
                'value')
        except Exception as es:
            print(f'Не смог проверить email "{es}"')
            return False

        return password_

    def loop_write_email(self):
        count = 0
        while True:
            if count > 5:
                print(f'Не смог авторизоваться вписать логин. Завершаюсь')
                return False

            res_email = self.check_email()

            if res_email != self.login:
                self.write_login()
                count += 1
            else:
                return True

    def loop_write_password(self):
        count = 0
        while True:
            if count > 5:
                print(f'Не смог авторизоваться вписать пароль. Завершаюсь')
                return False

            res_password = self.check_password()

            if res_password != self.password:
                self.write_password()

                count += 1
            else:
                return True

    def click_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@name, 'wp-submit')]").click()
        except Exception as es:
            print(f'Не смог авторизоваться click_login "{es}"')
            return False

        return True

    def click_remember(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@id, 'rememberme')]").click()
        except Exception as es:
            print(f'Не смог авторизоваться click_login "{es}"')
            return False

        return True

    def check_load_page(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@name, 'loginform')]")))
            return True
        except:
            return False

    def start_auth(self):
        check_load = self.check_load_page()

        if not check_load:
            return False

        res_write_login = self.loop_write_email()

        if not res_write_login:
            return False

        res_write_password = self.loop_write_password()

        if not res_write_password:
            return False

        res_click = self.click_remember()
        res_click = self.click_login()

        print(f'Ввёл данные авторизации вхожу')

        return True

    def check_auth(self):
        # time.sleep(1)
        try:
            """Первая проверка на авторизацию"""
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@name, 'loginform')]")

        except:

            return False

        return True

    def loop_auth(self):
        cont = 0
        while True:
            cont += 1
            if cont > 3:
                print(f'Не смог авторизоваться ')
                return False

            res_auth = self.check_auth()

            if res_auth:
                print(f'Проверяю авторизацию на {self.source_name}')
                res_auth = self.start_auth()

                time.sleep(3)

                if not res_auth:
                    print(f'Не могу авторизоваться')
                    time.sleep(60)
                    continue

            else:
                return True
