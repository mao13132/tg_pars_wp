from datetime import datetime


class SendlerOneCreate:

    def __init__(self, driver):
        self.TOKEN = ''
        self.ADMIN_TELEGRAM = '331583382'
        self.ADMIN_LIST = ['331583382']
        self.driver = driver

    def send_error_tg_img(self, msg=False):
        import os
        filename = f'screen{os.sep}{msg}_screen{datetime.now().strftime("%H_%M_%S")}.png'

        try:
            self.driver.save_screenshot(filename)
        except:
            pass
