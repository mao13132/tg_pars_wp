import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import getpass

from pathlib import Path


class CreatBrowser:

    def __init__(self):

        name_profile = 'Telegram'

        file_dir = Path(f"{os.getcwd()}/src/browser/profile/{name_profile}")

        user_system = getpass.getuser()

        options = webdriver.ChromeOptions()

        options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/114.0.0.0 Safari/537.36")

        options.add_argument("no-sandbox")

        options.add_argument("--remote-debugging-port=9222")

        options.add_argument("--headless")

        options.add_argument("window-size=1920,939")

        platform_to_os = platform.system()

        if platform_to_os == "Linux":
            path_dir = file_dir
            # path_dir = (f'/Users/{user_system}/Library/Application Support/Google/Chrome/{name_profile}')
            s = Service(r"browser/chromedriver.exe")
        else:
            path_dir = file_dir
            # path_dir = (f'C:\\Users\\{user_system}\\AppData\\Local\\Google\\Chrome\\User Data\\{name_profile}')
            s = Service(f"browse\\chromedriver.exe")

        options.add_argument(f"user-data-dir={path_dir}")  # Path to your chrome profile

        options.add_argument('--disable-dev-shm-usage')

        # prefs = {"profile.managed_default_content_settings.images": 2,
        #          "enable_do_not_track": True}
        #
        # options.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-infobars")
        options.add_argument("--ignore-certificate-errors")

        options.add_argument(
            "--disable-application-cache")
        options.add_argument(f"start-maximized")

        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(service=s, options=options)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
        })
