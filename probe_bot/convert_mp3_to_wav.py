import subprocess

# Путь к исходному файлу MP3
mp3_file = "5867884661_VOICE_KSMGL7A;TD.mp3"

# Путь к выходному файлу WAV
wav_file = "output.wav"

# Запуск внешней команды ffmpeg для преобразования файла
subprocess.call(["ffmpeg", "-i", mp3_file, wav_file])
