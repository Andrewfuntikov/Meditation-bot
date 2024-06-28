# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import aiogram.utils.markdown as md
import speech_recognition as sr
import subprocess
import datetime
from aiogram import Bot, types, Dispatcher
from probe_bot.main import BOT_TOKEN
from probe_bot.basis import download
logfile = str(
    datetime.date.today()) + '.log'  # формируем имя лог-файла  # Обратите внимание, что хранить токены в коде - не хорошо, здесь эта строка только для примера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def audio_to_text(dest_name: str):
    r = sr.Recognizer()
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio,
                                language="ru-RU")  # используя возможности библиотеки распознаем текст, так же тут можно изменять язык распознавания
    return result


@dp.message(content_types='voice')
async def get_audio_messages(message: types.Message):
    try:
        print("Started recognition...")
        file_info = await bot.get_file(message.voice.file_id)
        path = file_info.file_path  # Вот тут-то и полный путь до файла (например: voice/file_2.oga)
        fname = os.path.basename(path)  # Преобразуем путь в имя файла (например: file_2.oga)
        doc = await bot.download_file(file_info.file_path)
        with open(fname + '.oga', 'wb') as f:
            f.write(doc.content)  # вот именно тут и сохраняется сама аудио-мессага
        process = subprocess.run(['ffmpeg', '-i', fname + '.oga',
                                  fname + '.wav'])  # здесь используется страшное ПО ffmpeg, для конвертации .oga в .vaw
        result = audio_to_text(fname + '.wav')  # Вызов функции для перевода аудио в текст
        await message.answer(md.text(result))  # Отправляем пользователю, приславшему файл, его текст
    except sr.UnknownValueError as e:
        await message.answer("Прошу прощения, но я не разобрал сообщение, или оно поустое...")
    except Exception as e:
        await message.answer(
            "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
    finally:
        os.remove(fname + '.wav')
        os.remove(fname + '.oga')
