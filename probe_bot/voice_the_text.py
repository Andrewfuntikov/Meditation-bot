import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


# Функция для разбиения аудиофайла на части по тишине
def split_audio(audio_file):
    sound = AudioSegment.from_file(audio_file, format="wav")
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-40)

    return chunks


# Распознавание текста из аудиофайла
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    chunks = split_audio(audio_file)
    text = ""

    for chunk in chunks:
        with sr.AudioFile(chunk) as source:
            audio = recognizer.record(source)
            try:
                text += recognizer.recognize_google(audio, language='ru-RU') + " "
            except sr.UnknownValueError:
                pass

    return text


# Укажите путь к вашему аудиофайлу
audio_file = "ddt.wav"

transcribed_text = transcribe_audio(audio_file)
print("Текст из аудиофайла:")
print(transcribed_text)
