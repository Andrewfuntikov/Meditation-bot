from aiogram import Bot
from aiogram.types import Message
from pydub import AudioSegment
import os
import time

sounds = []


async def download(message: Message, bot: Bot):
    if message.content_type == 'audio':
        file_id = message.audio.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        user_id = message.from_user.id
        file_name = message.audio.file_name
        file_name_ex = f'{user_id}_{file_name}'
        time.sleep(10)
        await bot.download_file(file_path, file_name_ex)
        time.sleep(10)
        sound = AudioSegment.from_mp3(file_name_ex)
        time.sleep(10)
        sounds.append(sound)
        await message.answer(f'{sounds}')
    elif message.text.lower() == 'хватит':
        combined_sound = sum(sounds)
        user_id = message.from_user.id
        first_name_user = message.from_user.first_name
        user_name = message.from_user.username
        file_name_ex = f'{user_id}_AUDIO_{first_name_user}_{user_name}.mp3'
        time.sleep(10)
        combined_sound.export(file_name_ex, format="mp3")
        await bot.send_audio(chat_id=user_id, audio=file_name_ex)
        time.sleep(10)
        try:
            for file in sounds:
                os.remove(file)
            os.remove(file_name_ex)
            await bot.send_message('Спасибо что воспользовались моим ботом!')
        except Exception as exc:
            await bot.send_message(f'ERROR {exc}')
        finally:
            sounds.clear()
    else:
        await message.answer(f'УПС! Не тот файл')
