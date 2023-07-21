import asyncio
import time

from pyrogram import Client

from src.settings import *

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

        return True

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
              f'Тест сообщения:\n"{message.text}"\n'

        return msg

    async def in_black(self, lower_msg):
        for black in BLACKS:
            if black.lower() in lower_msg:
                return True

        return False

    async def check_msg_to_keybs(self, message):

        for keyb in KEYBOARDS:

            try:
                lower_keyb = keyb.lower()
                lower_msg = message.text.lower()
            except:
                lower_keyb = keyb
                lower_msg = ''

            if lower_keyb in lower_msg:

                in_black = await self.in_black(lower_msg)

                if in_black:
                    continue

                return keyb

        return False

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

    async def start_monitoring_chat(self, chat_id, link_chat):
        try:
            count = 0

            async for message in self.app.get_chat_history(chat_id):
                count += 1

                if count > count_message_new_chat:
                    msg = f'Достиг лимит на сообщения в чате {link_chat}. Останавливаюсь'
                    print(msg)
                    # await self._send_admin(msg)

                    return True

                target_keyb = await self.check_msg_to_keybs(message)

                print(f'{datetime.now().strftime("%H:%M:%S")} #{count} '
                      f'Обрабатываю сообщение ID: {message.id}')

                sql_res = self.BotDB.add_message(chat_id, message.id)

                if not sql_res:
                    print(f'{datetime.now().strftime("%H:%M:%S")} Все новые сообщения из чата {link_chat} обработаны')

                    return True

                if target_keyb:
                    resp_admin = await self.send_admin(message, target_keyb, chat_id)
                    if not resp_admin:
                        return False

                    time.sleep(30)

        except Exception as es:
            if 'CHANNEL_INVALID' in str(es):
                print(f'{datetime.now().strftime("%H:%M:%S")} Вы не подписаны на канал "{chat_id}" или бота исключили')
                return []

            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка при получении сообщений из "{chat_id}" "{es}"')
            return False

        print(f'Проверку {link_chat} закончил')

        return True

    async def loop_start_check(self, id_chat, link_chat):
        count = 0
        try_count = 3

        while True:
            count += 1
            if count > try_count:
                print(f'{datetime.now().strftime("%H:%M:%S")} Не смог промониторить чат "{id_chat}"')
                return False

            list_message = await self.start_monitoring_chat(id_chat, link_chat)

            if list_message == []:
                print(f'{datetime.now().strftime("%H:%M:%S")} Начинаю подписку на канал {id_chat}')
                res_join = await self.join_to_chat(link_chat)

                if not res_join:
                    return False

                if res_join:
                    print(f'{datetime.now().strftime("%H:%M:%S")} Успешно подписался на канал "{id_chat}"')

            if list_message:
                return list_message

    async def get_id_chat(self, name_link):
        try:
            name_chat = name_link.replace('https://t.me/', '')

            res_chat = await self.app.get_chat(name_chat)

            id_chat = res_chat.id

        except Exception as es:
            print(f'Не могу получить ID чата "{name_link}" "{es}"')

            return False

        return id_chat

    async def start_monitoring(self):
        """ТВХ"""

        for link_chat in CHANNELS:
            # for id_chat, _ in DATA_CHANELS.items():
            """Итерация списка с каналами"""

            id_chat = await self.get_id_chat(link_chat)

            print(f'')
            print(f'{datetime.now().strftime("%H:%M:%S")} Получаю сообщения из чата: {link_chat}')

            await self.loop_start_check(id_chat, link_chat)

        print(f'{datetime.now().strftime("%H:%M:%S")} Закончил мониторинг списка чатов')

        return True
