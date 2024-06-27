from gtts import gTTS
import os
import voice_the_text
mytext = format(voice_the_text.result)
audio = gTTS(text=mytext, lang="ru", slow=False)
audio.save("example.mp3")
os.system("start example.mp3")

