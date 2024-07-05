from aiogram import Bot
from aiogram.types import Message, FSInputFile
from pydub import AudioSegment
import random
import speech_recognition as sr
import subprocess
import os
import time

sounds_name = []
sounds_pydub_format = {}

r = sr.Recognizer()

random_symbol_list = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P','A', 'S',
    'D', 'F', 'G', 'H', 'J', 'K', 'L',':','Z', 'X', 'C', 'V',
    'B', 'N', 'M', "a", "b", "c", "d", "e", "f", "g", "h", "i",
    "j", "k", "l", "m","n", "o", "p", "q", "r", "s", "t", "u",
    "v", "w", "x", "y", "z"
]


async def download(message: Message, bot: Bot):
    if message.content_type == 'audio':
        user_id = message.from_user.id
        file_id = message.audio.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = message.audio.file_name
        file_name_ex = f'{user_id}_{file_name}_AUDIO.mp3'
        if file_name_ex.endswith('mp3'):
            pass
        else:
            while not file_name_ex.endswith('mp3'):
                random_symbol = random.sample(random_symbol_list, 10)
                random_symbol_string = ''.join(random_symbol)
                file_name_ex = f'{user_id}_VOICE_{random_symbol_string}.mp3'
        await bot.download_file(file_path, file_name_ex)
        sound = AudioSegment.from_mp3(file_name_ex)
        sounds_name.append(file_name_ex)
        if user_id not in sounds_pydub_format:
            sounds_pydub_format[user_id] = []
        sounds_pydub_format[user_id].append(sound)
        await message.answer('Спасибо за аудиосообщение! Теперь отправьте ещё, и я их склею.')
    elif message.content_type == 'voice':
        random_symbol = random.sample(random_symbol_list, 10)
        time.sleep(2)
        random_symbol_string = ''.join(random_symbol)
        time.sleep(2)
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        user_id = message.from_user.id
        file_path = file.file_path
        time.sleep(2)
        file_name_ex = f'{user_id}_VOICE_{random_symbol_string}.mp3'
        if file_name_ex.endswith('mp3'):
            pass
        else:
            while not file_name_ex.endswith('mp3'):
                random_symbol = random.sample(random_symbol_list, 10)
                random_symbol_string = ''.join(random_symbol)
                file_name_ex = f'{user_id}_VOICE_{random_symbol_string}.mp3'
        await bot.download_file(file_path, file_name_ex)
        wav_file = f"{user_id}_VOICE_{random_symbol_string}.wav"
        subprocess.call(["ffmpeg", "-i", file_name_ex, wav_file])
        os.remove(file_name_ex)
        subprocess.call(["ffmpeg", "-i", wav_file, file_name_ex])
        os.remove(wav_file)
        time.sleep(3)
        sound = AudioSegment.from_mp3(file_name_ex)
        sounds_name.append(file_name_ex)
        if user_id not in sounds_pydub_format:
            sounds_pydub_format[user_id] = []
        sounds_pydub_format[user_id].append(sound)
        await message.answer('Спасибо за голосовое! Теперь отправьте ещё, и я их склею.')
    elif message.text.lower() == 'хватит':
        user_id = message.from_user.id
        first_name_user = message.from_user.first_name
        user_name = message.from_user.username
        file_name_ex = f'{user_id}_AUDIO_FINAL_{first_name_user}_{user_name}.mp3'
        try:
            combined_sound = sum(sounds_pydub_format[user_id])
        except KeyError:
            await message.answer('Похоже склеивать нечего( Жду от вас аудио либо голосовые файлы :)')
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
            del sounds_pydub_format[user_id]
        except Exception as exc:
            await bot.send_message(5867884661,
                                   text=f'Не удалилсь файлы username = {user_name}, user_id = {user_id}')
        finally:
            sounds_pydub_format.clear()
            sounds_name.clear()
    else:
        await message.answer(f'🙊Файл не распознан, пришлите мне аудио сообщение формата mp3🙀')
