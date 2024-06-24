from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from probe_bot.handlers import StepsForm
import asyncio
import logging

from probe_bot.script import process_start_command, count_file, final

BOT_TOKEN = '6853584795:AAG1X_3nVDG9SzatOwKvlxooIpAsrBhYXrE'


# Создаем объекты бота и диспетчера
async def start_bot(bot: Bot):
    await bot.send_message(5867884661, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(5867884661, text='Бот запущен')


async def start():
    logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(process_start_command, Command(commands='fill'))
    dp.message.register(count_file, StepsForm.FILE_NAME)
    dp.message.register(final, StepsForm.COUNT_FILE )
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
# Запускаем поллинг
if __name__ == '__main__':
    asyncio.run(start())
