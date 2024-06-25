from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def first_cmd(message: Message, state: FSMContext):
    await message.answer('''👋Приветствую! Я бот, который поможет вам склеить два аудиосообщения формата mp3 в одно.
    Просто отправьте мне два аудиосообщения,и я их объединю 
    и вышлю вам обратно через некоторое время🕘.
А потом когда ваши аудио закончиться напишите "хватит"''')
#     await state.set_state(StepsForm.FILE_NAME)
#
#
# async def count_file(message: Message, state: FSMContext):
#     await message.answer(f'Твоё имя  {message.text}, введи количество файлов')
#     await state.update_data(FILE_NAME=message.text)
#     await state.set_state(StepsForm.COUNT_FILE)
#
#
# async def final(message: Message, state: FSMContext):
#     await message.answer(f'Количество файлов {message.text}')
#     await state.update_data(COUNT_FILE=message.text)
#     context_data = await state.get_data()
#     await message.answer(f'Все данные {context_data}')
#     await state.clear()
