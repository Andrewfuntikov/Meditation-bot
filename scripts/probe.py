"""Здесь будет рабочий проект без интеграции в тг бота"""
from pydub import AudioSegment

sounds = []
eee = input('Да/нет ')
while eee != 'нет':
    file_name = input('название файла: ')

    sound = AudioSegment.from_mp3(file_name)
    sounds.append(sound)

    eee = input('Да/нет ')

combined_sound = sum(sounds)
combined_sound.export("lox.mp3", format="mp3")

print('stop')
