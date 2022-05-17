from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.types.callback_query import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN, CHANNEL_ID
from states import Questions
from choice_buttons import *
from callback_datas import choice_callback
from valid_email_and_number import is_valid_number, is_valid_email

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'], state=None)
async def greeting(message: types.Message):
    await message.answer(f'Доброго времени суток, {message.from_user.first_name}.\nУ меня есть для вас пара вопросов, готовы на них ответить?', reply_markup=yes_no_kb)

    await Questions.yes_or_no.set()

@dp.callback_query_handler(yes_no_callback.filter(answer='yes'), state=Questions.yes_or_no)
async def answer_yes(message: types.Message, state: FSMContext):
    await state.update_data(answer1='yes')
    await bot.send_message(message.from_user.id, 'Отлично! Что тебя интересует?', reply_markup=choice_kb)
    await Questions.choice_area.set()

@dp.callback_query_handler(yes_no_callback.filter(answer='no'), state=Questions.yes_or_no)
async def answer_yes(message: types.Message):
    await bot.send_message(message.from_user.id, 'Всего доброго')

@dp.callback_query_handler(choice_callback.filter(area_name='fireplace'), state=Questions.choice_area)
async def choice_fireplace(call: CallbackQuery):
    if button_fireplace.text == 'Камины✔':
        button_fireplace.text = 'Камины❌'
    elif button_fireplace.text != 'Камины✔':
        button_fireplace.text = 'Камины✔'
    await call.message.edit_reply_markup(reply_markup=choice_kb)

@dp.callback_query_handler(choice_callback.filter(area_name='table'), state=Questions.choice_area)
async def choice_fireplace(call: CallbackQuery):
    if button_table.text == 'Столы✔':
        button_table.text = 'Столы❌'
    elif button_table.text != 'Столы✔':
        button_table.text = 'Столы✔'
    await call.message.edit_reply_markup(reply_markup=choice_kb)

@dp.callback_query_handler(choice_callback.filter(area_name='chair'), state=Questions.choice_area)
async def choice_fireplace(call: CallbackQuery):
    if button_chair.text == 'Стулья✔':
        button_chair.text = 'Стулья❌'
    elif button_chair.text != 'Стулья✔':
        button_chair.text = 'Стулья✔'
    await call.message.edit_reply_markup(reply_markup=choice_kb)


@dp.callback_query_handler(text='cancel', state=Questions.choice_area)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = ''
    if button_fireplace.text == 'Камины✔':
        answer += 'Камины '
    if button_table.text == 'Столы✔':
        answer += 'Столы'
    if button_chair.text == 'Стулья✔':
        answer += 'Стулья'
    await state.update_data(area=answer)
    await bot.send_message(message.from_user.id, 'Записал. Отправьте номер, чтобы наша команда могла с вами связаться.')
    await Questions.input_phone_number.set()

@dp.message_handler(state=Questions.input_phone_number)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    if is_valid_number(answer):
        await state.update_data(phone_number=answer)
        await message.answer('И email, на всякий случай.')
        await Questions.input_email.set()
    else:
        await message.answer('Вы ввели некорректный номер телефона, пожалуйста, повторите попытку.')

@dp.message_handler(state=Questions.input_email)
async def answer_q4(message: types.Message, state: FSMContext):
    data = await state.get_data()

    area = data.get('area')
    phone_number = data.get('phone_number')
    email = message.text
    if is_valid_email(email):
        await message.answer('Отлично! Скоро наша команда с вами свяжется.')

        await bot.send_message(CHANNEL_ID, f'Новое уведомление!\n'
                                           f'Пользователь: {message.from_user.id} | @{message.from_user.username}\n'
                                           f'Номер телефона: {phone_number}\n'
                                           f'Почта: {email}\n'
                                           f'Сфера: {area}')

        await state.reset_state()
    else:
        await message.answer('Вы ввели некорректный email, пожалуйста, повторите попытку.')



if __name__ == '__main__':
    executor.start_polling(dp)