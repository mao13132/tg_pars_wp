from datetime import datetime

from src.wp.wp_start import WpStart


class IterSite:
    def __init__(self, driver, BotDB):
        self.driver = driver
        self.BotDB = BotDB

    async def write_post(self, job):
        # TODO  итерация сайтов в JOB
        for site_data in job["sites"]:

            if site_data['site'] == '':
                print(f'Не указан сайт для публикации')
                continue
            if site_data['login'] == '':
                print(f'Нет логина для авторизации')
                continue
            if site_data['password'] == '':
                print(f'Нет пароля для авторизации')
                continue

            if job['posts'] == []:
                print(f'{site_data["site"]} нет постов к публикации')
                continue


            res_add_posts = WpStart(self.driver, self.BotDB, site_data, job).start_job_wp()

        return job
