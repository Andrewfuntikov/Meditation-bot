from aiogram import Bot
from aiogram.types import Message


async def download(message: Message, bot: Bot):
    if message.content_type == 'audio':
        file_id = message.audio.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        # Используем file_path из объекта file
        await bot.download_file(file_path, '123.mp3')
    else:
        await message.answer(f'УПС! Не тот файл')
