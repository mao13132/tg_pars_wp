from datetime import datetime


class IterChat:
    def __init__(self, telegram_core):
        self.telegram_core = telegram_core

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

            dict_post = await self.telegram_core.start_monitoring_chat(id_chat, link_chat)

            job['posts'].extend(dict_post)

            print()

        return job
