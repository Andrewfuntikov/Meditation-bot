from aiogram.fsm.context import FSMContext
from aiogram.types import Message, audio
from probe_bot.utils import StepsForm


async def first_cmd(message: Message, state: FSMContext):
    await message.answer('Привет введи своё имя!')
    await state.set_state(StepsForm.FILE_NAME)


async def count_file(message: Message, state: FSMContext):
    await message.answer(f'Твоё имя  {message.text}, введи количество файлов')
    await state.update_data(FILE_NAME=message.text)
    await state.set_state(StepsForm.COUNT_FILE)


async def final(message: Message, state: FSMContext):
    await message.answer(f'Количество файлов {message.text}')
    await state.update_data(COUNT_FILE=message.text)
    context_data = await state.get_data()
    await message.answer(f'Все данные {context_data}')
    await state.clear()
