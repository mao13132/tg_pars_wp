from src.wp.auth_wp import AuthWP

from src.wp.load_page import LoadPage
from src.wp.wp_add_post import WpAddPost
from telegram_debug import SendlerOneCreate


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

        core_wp_post_adder.check_modal_popup()

        link_add_post = self.site_data['site'].split('/')

        link_all_posts = f"https://{link_add_post[2]}/wp-admin/edit.php"

        link_add_post = f"https://{link_add_post[2]}/wp-admin/post-new.php"

        for post in self.posts_list:
            try:

                _text_title = post['title']

                count_try = 0

                while True:

                    count_try += 1

                    if count_try > 3:
                        print(f'Все попытки на публикацию исчерпал. Пропускаю "{post["text"]}"')

                        SendlerOneCreate(self.driver).send_error_tg_img(f'no_publish')

                        break

                    load_page = LoadPage(self.driver, link_add_post).loop_load_page(
                        f"//*[contains(@class, 'clear')]")

                    if not load_page:
                        print(f'Не удалось зайти на {self.site_data["site"]}')

                        SendlerOneCreate(self.driver).send_error_tg_img(f'no_open')

                        return False

                    insert_title = core_wp_post_adder.write_title(_text_title)

                    if post['media'] != []:
                        print(f'Публикую медиа')
                        res_send_media = core_wp_post_adder.insert_image_universal(post['media'])
                        print(f'Публикация медиа статус: {res_send_media}')
                        core_wp_post_adder.wait_load_media()

                        if not res_send_media:
                            SendlerOneCreate(self.driver).send_error_tg_img(f'error_preview')

                    try:
                        if 'jpg' in post['media'][0]:
                            print(f'Устанавливаю превью')
                            res_image_preview = core_wp_post_adder.loop_set_preview(post['media'][0])
                            print(f'Установка превью: {res_image_preview}')

                            if not res_image_preview:
                                SendlerOneCreate(self.driver).send_error_tg_img(f'error_preview')
                    except:
                        pass

                    if post['text'] != '':
                        print(f'Пишу текст')
                        res_write_text = core_wp_post_adder.write_text_in_frame(post['text'])
                        print(f'Написание текста: {res_write_text}')

                        if not res_write_text:
                            SendlerOneCreate(self.driver).send_error_tg_img(f'error_text')

                    if self.category != '':
                        print(f'Устанавливаю категорию')
                        res_insert_category = core_wp_post_adder.job_category(self.category)
                        print(f'Установка категории: {res_insert_category}')

                        if not res_insert_category:
                            SendlerOneCreate(self.driver).send_error_tg_img(f'error_category')

                    print(f'\n--- Публикую "{_text_title}"\n')

                    res_publish = core_wp_post_adder.loop_publish()

                    if res_publish:
                        print(f'Опубликовал запись {self.driver.current_url}')

                        break

                    SendlerOneCreate(self.driver).send_error_tg_img(f'no_publish_iter')

                    print(f'Перепроверка публикации...')

                    result_start_page = LoadPage(self.driver, link_all_posts).loop_load_page(
                        f"//*[contains(text(), 'Поиск записей')]")

                    check_post = core_wp_post_adder.check_title_post(f"//*[contains(text(), '{_text_title}')]")

                    if not check_post:
                        continue

                    draft_true = core_wp_post_adder.check_draft(_text_title)

                    if draft_true:
                        print(f'Найдена неопубликованная запись пробую опубликовать ещё раз')
                        continue

                    if check_post:
                        print(f'Перепроверка записи: запись уже существует')
                        break

                self.BotDB.add_message(post['chat_id'], _text_title, post['date_post'])
            except Exception as es:
                print(f'Пропуск поста из за возникновения проблем с сайтом. В базу не занёс "{es}"')
                continue

        print(f'Закончил публикации на {self.site_data["site"]}')

        return True
