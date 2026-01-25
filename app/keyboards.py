from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

help = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Админское')]],
                           resize_keyboard=True, #берёт минимальную длину клавиш
                           input_field_placeholder="Выбери пункт меню") #вместо набери сообщение будет это 🐨🍐)

admin_help = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Узнать id')],
                                           [KeyboardButton(text='💃 Создать пару 🕺'), KeyboardButton(text='Убрать пару(' )],
                                           [KeyboardButton(text='Отменить запрос')]], 
                            resize_keyboard=True, 
                            input_field_placeholder="Выбери пункт меню")

continue_pair_req = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да, продолжить', callback_data = 'cntue_pair_req'),
                                                   InlineKeyboardButton(text='Не, пусть будут', callback_data = 'no_cntue_pair_req')]])

pair_y_or_n = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да 🫂', callback_data='pairyes'),
                                                     InlineKeyboardButton(text='Нет ✋', callback_data='pairno')]]) #создать пару с тем-то тем-то?

cancel_pair_req = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отменить', callback_data = 'cancel_create_pail_req')]]) #перестать писать id пользователя?
