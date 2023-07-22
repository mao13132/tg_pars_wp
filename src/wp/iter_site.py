from datetime import datetime


class IterSite:
    def __init__(self, driver):
        self.driver = driver

    async def write_post(self, job):
        for link_site in job["sites"]:
            if job['posts'] == []:
                print(f'{link_site} нет постов к публикации')
                continue



            print(link_site)

        return job
