import random

from aiogram import Bot
from aiogram.types import Message, FSInputFile
from pydub import AudioSegment
import os
import time

sounds_pydub_format = []

sounds_name = []

random_symbol_list = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';',
    ':', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ','
]
# TODO всё в файле probe2.py и сделать интеграцию его себя


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
        # TODO Перевести файл voice_to_text.py на aiogram
        random_symbol = random.sample(random_symbol_list, 10)
        random_symbol_string = ''.join(random_symbol)
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        user_id = message.from_user.id
        file_path = file.file_path
        file_name_ex = f'{user_id}_VOICE_{random_symbol_string}.mp3'
        await bot.download_file(file_path, file_name_ex)
        sounds_name.append(file_name_ex)
        # sound = AudioSegment.from_mp3(file_name_ex)
        # sounds_pydub_format.append(sound)
        # await message.answer('Спасибо за аудиосообщение! Теперь отправьте ещё, и я их склею.')
        import speech_recognition as sr

        # Создаем объект распознавателя речи
        recognizer = sr.Recognizer()

        # Загружаем аудио файл
        audio_file = sr.AudioFile(file_name_ex)

        # Распознаем речь из аудио файла
        with audio_file as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Выводим текст
        print(text)
    # # Получаем файл голосового сообщения
    # file_id = message.voice.file_id
    # file = await bot.get_file(file_id)
    # user_id = message.from_user.id
    # file_path = file.file_path
    #
    # # Скачиваем файл голосового сообщения
    # voice_file = io.BytesIO()
    # await bot.download_file(file_path, voice_file)
    # voice_file.seek(0)
    #
    # # Распознаём речь
    # r = sr.Recognizer()
    # audio = sr.AudioFile(voice_file)
    # with audio as source:
    #     audio_data = r.record(source)
    # text = r.recognize_google(audio_data, language="ru-RU")
    #
    # # Отправляем распознанный текст пользователю
    # await message.answer(text)


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
            await bot.send_message(5867884661,
                                   text=f'Ботом воспользовался username = {user_name}, user_id = {user_id}')
        except Exception as exc:
            await message.answer('Ошибка! Похоже у меня технические шоколадки(')
            await bot.send_message(5867884661,
                                   text=f'Ошибка у пользователя  username = {user_name}, user_id = {user_id}, ошибка = {exc}')
        time.sleep(20)
        try:
            os.remove(file_name_ex)
            for file in sounds_name:
                os.remove(file)
        except Exception as exc:
            await bot.send_message(5867884661,
                                   text=f'Не удалилсь файлы username = {user_name}, user_id = {user_id}')
        finally:
            sounds_pydub_format.clear()
            sounds_name.clear()
    else:
        await message.answer(f'🙊Файл не распознан, пришлите мне аудио сообщение формата mp3🙀')
