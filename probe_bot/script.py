from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def first_cmd(message: Message, state: FSMContext):
    await message.answer('''👋Приветствую! Я бот, который поможет вам склеить два аудиосообщения формата mp3 в одно.
    Просто отправьте мне два аудиосообщения,и я их объединю 
    и вышлю вам обратно через некоторое время🕘.
А потом когда ваши аудио закончиться напишите "хватит"''')