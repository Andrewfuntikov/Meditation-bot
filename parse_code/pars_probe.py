from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def main():
    # Путь к файлам, которые нужно добавить
    file_paths = ('5867884661_VOICE_;B1J8PSI4X.mp3',
                  '5867884661_VOICE_HLDUNXYQTS.mp3')

    # Инициализация драйвера браузера
    driver = webdriver.Firefox()
    driver.get("https://audio-joiner.com/ru/")

    # Добавление треков на сайте
    add_track_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btn-file")))
    for file_path in file_paths:
        add_track_button.send_keys(file_path)

    # Нажатие кнопки "Сохранить"
    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "save-button")))
    save_button.click()

    # Ожидание окончания загрузки
    time.sleep(10)  # Можно увеличить время ожидания, если требуется

    # Закрытие драйвера
    driver.quit()


if __name__ == "__main__":
    main()
