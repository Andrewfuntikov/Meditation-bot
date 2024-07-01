from gtts import gTTS
import os

mytext = format(voice_the_text.result)
audio = gTTS(text=mytext, lang="ru", slow=False)
audio.save("example.mp3")
os.system("start example.mp3")
# TODO добавить в файл типа probe2.py
