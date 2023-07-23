from src.wp.auth_wp import AuthWP

from src.wp.load_page import LoadPage
from src.wp.wp_add_post import WpAddPost


class WpStart:
    def __init__(self, driver, BotDB, site_data, job):
        self.driver = driver
        self.BotDB = BotDB
        self.site_data = site_data
        self.posts_list = job['posts']
        self.category = job['category']

    def start_job_wp(self):

        core_wp_post_adder = WpAddPost(self.driver, self.BotDB, self.site_data)

        result_start_page = LoadPage(self.driver, self.site_data["site"]).loop_load_page(
            f"//*[contains(@class, 'clear')]")

        if not result_start_page:
            print(f'Не удалось зайти на {self.site_data["site"]}')
            return False

        res_auth = AuthWP(self.driver, self.site_data["site"], self.site_data['login'],
                          self.site_data['password']).loop_auth()

        if not res_auth:
            return False

        link_add_post = self.site_data['site'].split('/')

        link_add_post = f"https://{link_add_post[2]}/wp-admin/post-new.php"

        for post in self.posts_list:

            load_page = LoadPage(self.driver, link_add_post).loop_load_page(
                f"//*[contains(@class, 'clear')]")

            if not load_page:
                print(f'Не удалось зайти на {self.site_data["site"]}')
                return False

            res_write_title = core_wp_post_adder.write_title(post['text'])

            if post['media'] != []:
                print(f'Публикую медиа {self.site_data["site"]}')
                res_send_media = core_wp_post_adder.insert_image_universal(post['media'])

                core_wp_post_adder.wait_load_media()

            if 'jpg' in post['media'][0]:
                res_image_preview = core_wp_post_adder.insert_image_preview(post['media'][0])

            if post['text'] != '':
                res_write_text = core_wp_post_adder.write_text_in_frame(post['text'])

            if self.category != '':
                res_insert_category = core_wp_post_adder.click_category(self.category)

            core_wp_post_adder.click_publish()

            print(f'Публикую...')

            res_publish = core_wp_post_adder.check_publish()

            if res_publish:
                print(f'Опубликовал запись на {self.site_data["site"]}')

        print(f'Закончил публикации на {self.site_data["site"]}')

        return True