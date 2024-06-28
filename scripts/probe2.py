import speech_recognition as sr

# Создаем объект Recognizer
r = sr.Recognizer()

# Определяем путь к аудиофайлу
audio_file = "krim_wav.wav" # TODO добавить конвертер скачинового файла .mp3 в .wav только с этим файлом можно работать
# import pydub
# sound = pydub.AudioSegment.from_wav('''Путь к wav''')
# sound.export("*Путь для нового файла*//*Желаемое название для файла*.mp3", format="mp3")
# Считываем аудиофайл
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

try:
    # Преобразуем записанный звук в текст
    text = r.recognize_google(audio, language="ru")
    print("Вы сказали: " + text)
except sr.UnknownValueError:
    print("Извините, не удалось распознать речь.")
except sr.RequestError as e:
    print("Ошибка сервиса распознавания речи; {0}".format(e))
