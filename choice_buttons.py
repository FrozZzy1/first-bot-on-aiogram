from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_datas import choice_callback, yes_no_callback

button_fireplace = InlineKeyboardButton(text='Камины', callback_data=choice_callback.new(area_name='fireplace'))
button_table = InlineKeyboardButton(text='Столы', callback_data=choice_callback.new(area_name='table'))
button_chair = InlineKeyboardButton(text='Стулья', callback_data=choice_callback.new(area_name='chair'))
button_cancel = InlineKeyboardButton(text='Выбор закончен', callback_data='cancel')

choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            button_fireplace,
            button_table,
            button_chair,
        ],
        [
            button_cancel
        ]
    ]
)

yes_no_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text='Да', callback_data=yes_no_callback.new(answer='yes')),
        InlineKeyboardButton(text='Нет', callback_data=yes_no_callback.new(answer='no')),
        ]
    ]
)
