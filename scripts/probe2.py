import os

from aiogram import Bot, Dispatcher, types
from aiogram import Bot
from aiogram.types import FSInputFile


async def download_audio(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    await bot.send_voice(voice=FSInputFile("downloaded_audio.mp3"), chat_id=user_id)
