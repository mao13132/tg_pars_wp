from src.wp.iter_site import IterSite


class StartIterSite:
    def __init__(self, driver, BotDB, job_dict):
        self.driver = driver
        self.BotDB = BotDB
        self.job_dict = job_dict

    async def start_iter(self):
        #TODO итерация главных словарей
        for job in self.job_dict:
            print(f'Начинаю процедуру постинга: "{job["name"]}"')

            post_dict = await IterSite(self.driver, self.BotDB).write_post(job)

        return self.job_dict
