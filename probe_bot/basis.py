from aiogram import Bot
from aiogram.types import Message, FSInputFile
from pydub import AudioSegment
import os
import time

sounds_pydub_format = []

sounds_name = []


async def download(message: Message, bot: Bot):
    if message.content_type == 'audio':
        file_id = message.audio.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        user_id = message.from_user.id
        file_name = message.audio.file_name
        file_name_ex = f'{user_id}_{file_name}'
        await bot.download_file(file_path, file_name_ex)
        sound = AudioSegment.from_mp3(file_name_ex)
        sounds_name.append(file_name_ex)
        sounds_pydub_format.append(sound)
        await message.answer('Спасибо за аудиосообщение! Теперь отправьте ещё, и я их склею.')
    elif message.content_type == 'voice':
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        user_id = message.from_user.id
        file_path = file.file_path
        file_name_ex = f'{user_id}_VOICE_.mp3'
        await bot.download_file(file_path, file_name_ex)
        sound = AudioSegment.from_mp3(file_name_ex)
        sounds_name.append(file_name_ex)
        sounds_pydub_format.append(sound)
        await message.answer('Спасибо за аудиосообщение! Теперь отправьте ещё, и я их склею.')
    elif message.text.lower() == 'хватит':
        combined_sound = sum(sounds_pydub_format)
        user_id = message.from_user.id
        first_name_user = message.from_user.first_name
        user_name = message.from_user.username
        file_name_ex = f'{user_id}_AUDIO_{first_name_user}_{user_name}.mp3'
        combined_sound.export(file_name_ex, format="mp3")
        try:
            await bot.send_audio(audio=FSInputFile(file_name_ex), chat_id=user_id)
            await message.answer('Спасибо что воспользовались моим ботом!')
            await bot.send_message(5867884661, text=f'Ботом воспользовался username = {user_name}, user_id = {user_id}')
        except Exception as exc:
            print(f'ERROR ERROR ERROR ERROR {exc}')
            await message.answer('Ошибка! Похоже у меня технические шоколадки(')
        time.sleep(20)
        try:
            os.remove(file_name_ex)
            for file in sounds_name:
                os.remove(file)
        except Exception as exc:
            print(f'ERROR {exc}')
        finally:
            sounds_pydub_format.clear()
            sounds_name.clear()
    else:
        await message.answer(f'🙊Файл не распознан, пришлите мне аудио сообщение формата mp3🙀')
