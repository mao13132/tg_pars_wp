from src.telegram.iter_chat import IterChat


class StartIterTgChat:
    def __init__(self, telegram_core, BotDB, job_dict):
        self.telegram_core = telegram_core
        self.BotDB = BotDB
        self.job_dict = job_dict

    async def start_iter(self):
        for job in self.job_dict:
            print(f'Начинаю обработку {job["name"]}')

            post_dict = await IterChat(self.telegram_core).get_posts(job)

        return self.job_dict
