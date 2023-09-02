import time

from pyrogram import Client

from settings import *

from datetime import datetime


class MonitoringTelegram:
    def __init__(self, sessions_patch, BotDB):
        self.BotDB = BotDB
        self.path = sessions_patch + f'/{API_ID}'

    async def start_tg(self):

        print(f'{datetime.now().strftime("%H:%M:%S")} Инициализирую вход в аккаунт {API_ID}')

        try:
            self.app = Client(self.path, API_ID, API_HASH)

            await self.app.start()

        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка при авторизации ({API_ID}) "{es}"')

            return False

        return self

    async def join_to_chat(self, chat):
        try:
            name_chat = chat.replace('https://t.me/', '')

            response = await self.app.join_chat(name_chat)
        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка join_chat ()  "{es}"')

            return False

        return True

    async def formated_msg(self, message, target_keyb, chat_id):
        try:
            first_name = message.from_user.first_name
        except:
            first_name = 'Не указан'
        try:
            last_name = message.from_user.last_name
        except:
            last_name = 'Не указан'

        try:
            username = f'https://t.me/{message.from_user.username}'
        except:
            username = 'Не указан'

        try:
            id_msg = message.from_user.id
        except:
            id_msg = 'Не указан'

        msg = f'Monitoring Bot: найден ключевик "{target_keyb}"\n\n' \
              f'Чат: {chat_id}\n\n' \
              f'Автор сообщения: {first_name} {last_name}\n\n' \
              f'Дата сообщения {message.date}\n\n' \
              f'ID: {id_msg} профиль: {username}\n\n' \
              f'Ссылка на сообщение {message.link}\n\n' \
              f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n' \
              f'Тест сообщения:\n"{message.caption}"\n'

        return msg

    async def _send_admin(self, msg):
        for admin_ in ADMIN:

            try:
                send_ = await self.app.send_message(admin_, msg, disable_web_page_preview=True)
            except Exception as es:
                if 'PEER_ID_INVALID' in str(es):
                    print(f'{datetime.now().strftime("%H:%M:%S")} Перепроверьте логин админа. Формат: @username')
                    continue
                print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка оповещения админа {admin_} "{es}"')
                continue

        return True

    async def send_admin(self, message, target_keyb, chat_id):
        msg = await self.formated_msg(message, target_keyb, chat_id)

        resp = await self._send_admin(msg)

        if resp:
            print(f'{datetime.now().strftime("%H:%M:%S")} Отправил пост админу. Встаю на паузу')

            return True

        return False

    async def download_media(self, list_rows_media):
        good_media_list = []

        text_message = ''

        for row in list_rows_media:
            if row.caption:
                text_message = row.caption

            good_media = await self.app.download_media(row)

            good_media_list.append(good_media)

        return good_media_list, text_message

    async def start_monitoring_chat(self, chat_id, link_chat, stop_date_post, main_stop_date):

        stop_title_list = []

        id_media_list = []

        good_post = []

        count = 1

        async for message in self.app.get_chat_history(chat_id):
            # sql_res = self.BotDB.add_message(chat_id, message.id)

            date_post = message.date

            if stop_date_post == '':
                if main_stop_date != '':
                    if date_post < main_stop_date:
                        continue
            else:
                if date_post < stop_date_post:
                    continue

            one_post = {}

            media_group_id = message.media_group_id

            if media_group_id:
                if media_group_id in id_media_list:
                    continue

                id_media_list.append(media_group_id)

                media_ = await message.get_media_group()

                good_media_list, text_msg = await self.download_media(media_)

            else:
                try:
                    good_media_list = [await self.app.download_media(message)]
                except:
                    good_media_list = []

                text_msg = message.caption
                if not text_msg:
                    text_msg = message.text

            if not text_msg and good_media_list == []:
                continue

            from src.wp.formated_title import get_title
            one_post['title'] = get_title(text_msg)

            if one_post['title'] in stop_title_list:
                continue

            stop_title_list.append(one_post['title'])

            one_post['date_post'] = date_post

            sql_res = self.BotDB.exist_message(chat_id, one_post['title'], one_post['date_post'])

            if sql_res:
                count += 1

                continue

            one_post['text'] = text_msg
            one_post['media'] = good_media_list
            one_post['chat_id'] = chat_id
            one_post['source'] = link_chat

            good_post.append(one_post)

            print(f'{datetime.now().strftime("%H:%M:%S")} #{count} '
                  f'Обработал сообщение ID: {message.id} от {date_post}')

            count += 1

            if count > count_message_new_chat:
                msg = f'Достиг лимит на сообщения в чате {link_chat}. Останавливаюсь'
                print(msg)

                return good_post

        return good_post

    async def get_id_chat(self, name_link):
        try:
            name_chat = name_link.replace('https://t.me/', '')



        except Exception as es:
            print(f'Не могу получить вырезать имя чата "{name_link}" "{es}"')

            return False

        while True:
            try:
                res_chat = await self.app.get_chat(name_chat)
            except Exception as es:
                print(f'Исключения при получение ID чат {es}')
                return False

            id_chat = res_chat.id

            return id_chat
