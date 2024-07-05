import sqlite3
import telebot
import threading
import time
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем соединение с базой данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем бота
bot = telebot.TeleBot("6853584795:AAG1X_3nVDG9SzatOwKvlxooIpAsrBhYXrE")

# Создаем главное меню
main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add('Оставить отзыв', 'Проверить статус аккаунта', 'Найти отзывы о блогере')

# Создаем меню для выбора типа рекламы
ad_type_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
ad_type_menu.add('Инст сторис', 'Инст рилс', 'YouTube подкаст', 'ТГ эфир', 'ТГ посты')

# Создаем меню для выбора количества звезд
stars_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
stars_menu.add('1', '2', '3', '4', '5')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(bot, message, cursor):
    # Приветствуем пользователя
    bot.send_message(message.chat.id,
                     "Привет! 👋\nЯ бот, который помогает собирать анонимные отзывы о блогерах. За них ты сможешь заработать скидку на рекламу у блогеров в нашем сервисе, а также помочь другим!\n\nДавай сейчас мы с тобой познакомимся, чтобы закрепить за тобой скидку!\n\n- Как тебя зовут? (напиши свое имя и фамилию)")

    # Регистрируем пользователя в базе данных
    cursor.execute(
        "INSERT INTO users (chat_id, first_name, last_name, stars, rank, discount) VALUES (?, ?, ?, ?, ?, ?)",
        (message.chat.id, None, None, 0, 0, 0))
    conn.commit()

    # Отправляем приветственное сообщение и главное меню
    bot.send_message(message.chat.id,
                     "Ты такой зайка. Держи 5 звездочек за ответы на вопросы! 🌟🌟🌟🌟🌟\n\nУ нас здесь есть система, чем больше у тебя звезд, тем больше скидка на покупку рекламы через наш сервис!\n\nРанг 1- 1% (начинающий закупщик)- 55 баллов\nРанг 2- 3% (средний закупщик)- 555 баллов\nРанг 3- 5% (профессиональный закупщик)- 1555 баллов\n\n(Программа считает количество баллов и сама дает человеку ранг, в основном меню можно посмотреть количество баллов)")
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu)


# Обработчик сообщений с именем и фамилией пользователя
@bot.message_handler(content_types=['text'])
def get_name(message):
    # Получаем имя и фамилию пользователя
    name, last_name = message.text.split()

    # Обновляем данные пользователя в базе данных
    cursor.execute("UPDATE users SET first_name = ?, last_name = ? WHERE chat_id = ?",
                   (name, last_name, message.chat.id))
    conn.commit()

    # Отправляем приветственное сообщение и главное меню
    bot.send_message(message.chat.id,
                     f"Ты такой зайка. Держи 5 звездочек за ответы на вопросы! 🌟🌟🌟🌟🌟\n\nУ нас здесь есть система, чем больше у тебя звезд, тем больше скидка на покупку рекламы через наш сервис!\n\nРанг 1- 1% (начинающий закупщик)- 55 баллов\nРанг 2- 3% (средний закупщик)- 555 баллов\nРанг 3- 5% (профессиональный закупщик)- 1555 баллов\n\n(Программа считает количество баллов и сама дает человеку ранг, в основном меню можно посмотреть количество баллов)")
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu)


# Обработчик кнопки "Оставить отзыв"
@bot.message_handler(func=lambda message: message.text == 'Оставить отзыв')
def leave_review(message):
    # Отправляем сообщение с просьбой прислать имя и фамилию блогера
    bot.send_message(message.chat.id, "Пришли имя и фамилию блогера")


# Обработчик сообщения с именем и фамилией блогера
@bot.message_handler(content_types=['text'])
def get_blogger_name(message):
    # Получаем имя и фамилию блогера
    blogger_name = message.text

    # Создаем сообщение с вопросами для отзыва
    review_questions = """Супер! Ответь на обязательные вопросы, чтобы получить максимальное количество баллов!

1. Стоимость рекламы?
2. Окупилась ли интеграция, если да, то сколько заработал?
3. Насколько тебе понравилось общение с блогером?
4. Какой был приход подписчиков?
5. Во сколько вышел один подписчик?

6. Какой это был вид рекламы (инст сторис, инст
"""

    # Отправляем сообщение с вопросами
    bot.send_message(message.chat.id, review_questions)


# Обработчик сообщения с текстом отзыва
@bot.message_handler(contenttypes='text')
def getreview(message):
    # Получаем текст отзыва
    review = message.text

    # Создаем сообщение с просьбой прикрепить запись экрана с перепиской с блогером
    screenshotrequest = """Пожалуйста, прикрепи запись экрана с перепиской с блогером для подтверждения своего отзыва и чтобы обезопасить наш сервис (если что мы это запись никому не покажем)"""

    # Отправляем сообщение с просьбой прикрепить запись экрана
    bot.sendmessage(message.chat.id, screenshotrequest)


# Обработчик сообщения с записью экрана
@bot.message_handler(contenttypes='video')
def getscreenshot(message):
    # Получаем путь к файлу с записью экрана
    screenshotpath = message.video.filepath

    # Скачиваем файл с записью экрана
    fileinfo = bot.get_file(screenshotpath)
    downloadedfile = bot.download_file(fileinfo.filepath)

    # Сохраняем файл с записью экрана на диск
    with open('screenshot.mp4', 'wb') as f:
        f.write(downloadedfile)

    # Создаем сообщение с благодарностью за отзыв и количеством начисленных звезд
    thankyoumessage = "Спасибо зайчик, вот твои 5 звезд. Остальные 45 пришлем после модерации твоего сообщения 🌟🌟🌟🌟🌟"

    # Отправляем сообщение с благодарностью за отзыв
    bot.send_message(message.chat.id, thankyoumessage)

    # Добавляем отзыв в базу данных
    cursor.execute(
        "INSERT INTO reviews (bloggername, cost, roi, communication, subscribers, subscribercost, adtype, review, screenshot, stars) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (bloggername, None, None, None, None, None, None, review, screenshotpath, 5))
    conn.commit()


# Обработчик кнопки "Проверить статус аккаунта"
@bot.message_handler(func=lambda message: message.text == 'Проверить статус аккаунта')
def checkstatus(message):
    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT firstname, lastname, stars, rank, discount FROM users WHERE chatid = ?", (message.chat.id,))
    userdata = cursor.fetchone()

    # Формируем сообщение со статусом аккаунта
    statusmessage = f"Привет, {userdata[0]} {userdata[1]}!\n\nТвой баланс: {userdata[2]} звезд 🌟\nТвой статус: {userdata[3]}\nТвоя скидка: {userdata[4]}%"

    # Отправляем сообщение со статусом аккаунта
    bot.send_message(message.chat.id, statusmessage)


# Обработчик кнопки "Найти отзывы о блогере"
@bot.message_handler(func=lambda message: message.text == 'Найти отзывы о блогере')
def find_reviews(message):
    # Отправляем сообщение с просьбой ввести имя и фамилию блогера
    bot.send_message(message.chat.id, "Введи имя и фамилию блогера")


# Обработчик сообщения с именем и фамилией блогера
@bot.message_handler(content_types=['text'])
def get_blogger_name_for_search(message):
    # Получаем имя и фамилию блогера
    blogger_name = message.text

    # Получаем отзывы о блогере
    cursor.execute("SELECT review FROM reviews WHERE blogger_name = ?", (blogger_name,))
    reviews = cursor.fetchall()

    # Формируем сообщение с отзывами
    reviews_message = "Отзывы о блогере {}:\n\n".format(blogger_name)
    for review in reviews:
        reviews_message += "- {}\n".format(review[0])

    # Отправляем сообщение с отзывами
    bot.send_message(message.chat.id, reviews_message)


# Функция для обработки обновлений в отдельном потоке
def threaded_polling(bot):
    while True:
        try:
            updates = bot.get_updates()

            for update in updates:
                # Создаем новый курсор в потоке обработчика обновлений
                cursor = conn.cursor()

                # Обрабатываем обновление
                start(bot, update, cursor)

                # Закрываем курсор
                cursor.close()
        except Exception as e:
            logging.error(e)
            time.sleep(1)


# Запускаем бота в отдельном потоке
threading.Thread(target=threaded_polling, args=(bot,)).start()
