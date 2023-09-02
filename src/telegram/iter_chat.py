from datetime import datetime

from settings import STOP_DATE


class IterChat:
    def __init__(self, telegram_core):
        self.telegram_core = telegram_core

    async def parser_date(self, _date):

        try:
            stop_date_post = datetime.strptime(_date, '%d.%m.%Y')
            print(f'- Включен режим пропуска постов до {_date}')
        except:
            stop_date_post = ''

        try:
            main_date_stop = datetime.strptime(STOP_DATE, '%d.%m.%Y')

            if stop_date_post == '':
                print(f'- Включен режим пропуска постов до {STOP_DATE}')
        except:
            main_date_stop = ''

        return stop_date_post, main_date_stop

    async def get_posts(self, job):
        job['posts'] = []

        for link_chat in job["channels"]:
            if link_chat == '':
                print(f'Не указан телеграм канал донор - пропуск')
                continue

            id_chat = await self.telegram_core.get_id_chat(link_chat)

            if not id_chat:
                return False

            print(f'\n{datetime.now().strftime("%H:%M:%S")} Получаю сообщения из чата: {link_chat}')

            stop_date_post, main_stop_date = await self.parser_date(job['date'])

            dict_post = await self.telegram_core.start_monitoring_chat(id_chat, link_chat,
                                                                       stop_date_post, main_stop_date)

            job['posts'].extend(dict_post)

            print()

        return job
