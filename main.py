import asyncio
import os

from sql.bot_connector import BotDB

from src.monitoring_telegram import MonitoringTelegram

from src.settings import CHECK_EVERY


async def main():

    sessions_path = os.path.join(os.path.dirname(__file__), 'src', 'sessions')

    bot_core = MonitoringTelegram(sessions_path, BotDB)

    res_auth = await bot_core.start_tg()

    if not res_auth:
        return False

    print(f'Успешно авторизовался')

    await bot_core._send_admin('Начинаю работу')

    while True:

        await bot_core.start_monitoring()

        print(f'Засыпаю на {int(CHECK_EVERY)} минут')

        await asyncio.sleep(CHECK_EVERY * 60)


if __name__ == '__main__':

    try:
        asyncio.run(main())

    finally:

        print(f'Бот остановлен')
