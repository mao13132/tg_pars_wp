import asyncio

import os

import time

import logging

from settings import CHANNELS_AND_SITE, CHECK_EVERY

from sql.bot_connector import BotDB
from src.browser.createbrowser import CreatBrowser

from src.start_iter_chat import StartIterTgChat
from src.start_iter_site import StartIterSite

from src.telegram.monitoring_telegram import MonitoringTelegram

logging.basicConfig(level=logging.CRITICAL)


async def main():
    sessions_path = os.path.join(os.path.dirname(__file__), 'src', 'sessions')

    telegram_core = await MonitoringTelegram(sessions_path, BotDB).start_tg()

    await telegram_core._send_admin('Начинаю работу')

    while True:

        job_dict = CHANNELS_AND_SITE

        dict_posts = await StartIterTgChat(telegram_core, BotDB, job_dict).start_iter()

        if not dict_posts:
            try:
                telegram_core = await MonitoringTelegram(sessions_path, BotDB).start_tg()
            except:
                return False

            continue

        count_post = sum([len(x['posts']) for x in dict_posts])

        if count_post == 0:
            print(f'Новых постов для публикации нет. Ожидание новых постов в Telegram')
            time.sleep(CHECK_EVERY * 60)
            continue

        browser_core = CreatBrowser()

        if not browser_core:
            print(f'Ошибка: не смог создать браузер')
            return False

        dict_pw = await StartIterSite(browser_core.driver, BotDB, job_dict).start_iter()

        print(f'Закончил, делаю паузу. В ожидании новых постов в Telegram')

        browser_core.driver.quit()

        time.sleep(CHECK_EVERY * 60)


if __name__ == '__main__':

    try:
        asyncio.run(main())

    finally:

        print(f'Бот остановлен')
