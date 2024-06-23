"""Здесь будет рабочий проект без интеграции в тг бота"""
from pydub import AudioSegment

sounds = []  # Создаем пустой список для хранения аудиофайлов
eee = input('Да/нет ')
while eee != 'нет':
    # Запросить название аудиофайла
    file_name = input('название файла: ')

    # Загружаем аудиофайл и добавляем его в список
    sound = AudioSegment.from_mp3(file_name)
    sounds.append(sound)

    eee = input('Да.нет ')

# Склеиваем все аудиофайлы из списка
combined_sound = sum(sounds)
# Экспортируем склеенный аудиофайл
combined_sound.export("lox.mp3", format="mp3")

print('stop')