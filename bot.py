from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from pydub import AudioSegment
from aiogram.types import FSInputFile
import logging
import asyncio
import os

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6853584795:AAG1X_3nVDG9SzatOwKvlxooIpAsrBhYXrE")
# Диспетчер
dp = Dispatcher()

sounds = []


# хендлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет этот бот может складывать аудио /sum")


@dp.message(Command("sum"))
async def dowload_audio(message: types.Message):
    file_name = await message.answer("Введите название итогового файла:")
    if file_name is not None:
        await message.answer("Отправляй аудио!")
    if message.audio:
        await bot.download(message.audio.file_id, file_name)
        sound = AudioSegment.from_mp3(file_name)
        sounds.append(sound)
        await message.answer(f"Так {len(sounds)} есть давай ещё")
    else:
        await message.answer('Отправьте мне аудио')


async def cmd_sum(message: types.Message, file_name):
    # Склеиваем все аудиофайлы из списка
    combined_sound = sum(sounds)

    # Экспортируем склеенный аудиофайл
    combined_sound.export(f'{file_name}.mp3', format="mp3")
    audio = FSInputFile(f'{file_name}.mp3')  # используй FSInputFile вместо open
    await bot.send_audio(message.from_user.id, audio)

    for file in sounds:
        os.remove(file)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
