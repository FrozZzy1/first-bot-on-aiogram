from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN, CHANNEL_ID
from utils import Questions

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


button_areas = ReplyKeyboardMarkup()
button_areas.add(KeyboardButton('Камины')).add(
    KeyboardButton('Столы')).add(
    KeyboardButton('Стулья'))


@dp.message_handler(commands=['start'], state=None)
async def greeting(message: types.Message):
    await message.answer(f'Доброго времени суток, {message.from_user.first_name}.\nУ меня есть для вас пара вопросов, готовы на них ответить?')

    await Questions.Q1.set()

@dp.message_handler(state=Questions.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.lower() == 'да':

        await state.update_data(answer1=answer)
        await message.answer('Отлично! Что тебя интересует?', reply_markup=button_areas)
        await Questions.Q2.set()

    elif answer.lower() == 'нет':
        await message.answer('Всего доброго')

@dp.message_handler(state=Questions.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(area=answer)
    await message.answer('Записал. Отправьте номер, чтобы наша команда могла с вами связаться.', reply_markup=ReplyKeyboardRemove())
    await Questions.Q3.set()

@dp.message_handler(state=Questions.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(phone_number=answer)
    await message.answer('И email, на всякий случай.')
    await Questions.Q4.set()

@dp.message_handler(state=Questions.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    data = await state.get_data()

    area = data.get('area')
    phone_number = data.get('phone_number')
    email = message.text

    await message.answer('Отлично! Скоро наша команда с вами свяжется.')

    await bot.send_message(CHANNEL_ID, f'Новое уведомление!\n'
                                       f'Пользователь: {message.from_user.id} | @{message.from_user.username}\n'
                                       f'Номер телефона: {phone_number}\n'
                                       f'Почта: {email}\n'
                                       f'Сфера: {area}')

    await state.reset_state()



if __name__ == '__main__':
    executor.start_polling(dp)