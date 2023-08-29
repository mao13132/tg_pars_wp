from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoadPage:
    def __init__(self, driver, url):
        self.url = url
        self.driver = driver
        self.source_name = url

    def approve_close(self):
        try:
            alert_obj = self.driver.switch_to.alert
            alert_obj.accept()
            self.driver.switch_to.default_content()
        except:
            return False

        return True

    def load_page(self, url):
        try:
            self.driver.get(url)
            self.approve_close()
            return True
        except TimeoutException:
            return False
        except Exception as es:
            return False

    def __check_load_page(self, _xpatch):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:
            return False

    def loop_load_page(self, _xpatch):
        count = 0
        count_ower = 60

        self.driver.set_page_load_timeout(30)

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                continue

            check_page = self.__check_load_page(_xpatch)

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True
