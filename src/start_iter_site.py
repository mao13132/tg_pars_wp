from src.wp.iter_site import IterSite


class StartIterSite:
    def __init__(self, driver, BotDB, job_dict):
        self.driver = driver
        self.BotDB = BotDB
        self.job_dict = job_dict

    async def start_iter(self):
        for job in self.job_dict:
            print(f'Начинаю обработку {job["name"]}')

            post_dict = await IterSite(self.driver).write_post(job)

        return self.job_dict
