from datetime import datetime

import requests

import base64


class SendlerOneCreate:
    """from telegram_debug import *
SendlerOneCreate(self.driver).send_error_tg_img()"""

    def __init__(self, driver):
        self.TOKEN = '6181022163:AAHQKUtmTp0HSbDooEq4k8zUYVCMCj3mIUc'
        self.ADMIN_TELEGRAM = '331583382'
        self.ADMIN_LIST = ['331583382']
        self.driver = driver

    def send_error_tg_img(self, msg=False):
        import os
        filename = f'screen{os.sep}{datetime.now().strftime("%H_%M_%S")}.png'

        self.driver.save_screenshot(filename)

        # self.send_image(filename, msg)


    def send(self, file):
        # file = open(r'media/ads.jpg', 'rb')
        open_files = {'photo': base64.b64decode(file)}
        cap = {'caption': 'test'}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendPhoto?chat_id=" + self.ADMIN_TELEGRAM

        # requests.post(self.api_url + method, data={'chat_id': chat_id}, files={'document': document})

        requests.post(url_req, files=open_files, data=cap)

        file.close()

        print(f"Отправил объявление в телеграм")

    # TODO написать что бы входящий поток был driver_page_source and driver.screen_shoot
    def send_html_and_screen(self, file):

        file_in = open(file, 'rb')
        open_files = {'document': file_in}

        # cap = {'caption': 'test'}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendDocument?chat_id=" + self.ADMIN_TELEGRAM

        response = requests.post(url_req, files=open_files)

        file_in.close()

        print(f"Отправил html в телеграм")

    # if __name__ == '__main__':

    def send_image(self, filename, msg=False):
        for admin_ in self.ADMIN_LIST:


            file = open(filename, 'rb')

            open_files = {'photo': file}

            if msg:
                cap = {'caption': msg}
            else:
                cap = {'caption': 'Debuger'}

            url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendPhoto?chat_id=" + admin_

            response = requests.post(url_req, files=open_files, data=cap)

            file.close()

        # print(f"Отправил изображение в телеграм")

    def save_text(self, text):

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendMessage" + "?chat_id=" + \
                  self.ADMIN_TELEGRAM + "&text=" + text

        results = requests.get(url_req)


