import random
import speech_recognition as sr
import subprocess
from gtts import gTTS
import os
import time

r = sr.Recognizer()

mp3_file = "5867884661_VOICE_KSMGL7A;TD.mp3"

wav_file = "output.wav"

subprocess.call(["ffmpeg", "-i", mp3_file, wav_file])
random_symbol_list = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';',
    ':', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ','
]
random_symbol = random.sample(random_symbol_list, 10)
random_symbol_string = ''.join(random_symbol)


def startConvertion(path='output.wav', lang='ru-IN'):
    with sr.AudioFile(path) as source:
        audio_file = r.record(source)
        text_out = r.recognize_google(audio_file, language=lang)

    mytext = text_out
    audio = gTTS(text=mytext, lang="ru", slow=False)
    audio.save(f"{random_symbol_string}.mp3")
    os.system(f"start {random_symbol_string}.mp3")
    time.sleep(10)
    try:
        os.remove("output.wav")
    except Exception as exc:
        print(f'ERROR ERROR {exc}')


startConvertion()
