from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           CopyTextButton)

help = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Админское')],
                                       [KeyboardButton(text = 'Игровоеове')]],
                           resize_keyboard=True, #берёт минимальную длину клавиш
                           input_field_placeholder="Выбери пункт меню") #вместо набери сообщение будет это 🐨🍐)

admin_help = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🤨 Узнать id 🧐')],
                                           [KeyboardButton(text='💃 Создать пару 🕺'), KeyboardButton(text='✋ Убрать пару( ✋' )],
                                           [KeyboardButton(text='❓ Мои запросы ❓')],
                                           [KeyboardButton(text='❌ Отменить запрос ❌')]], 
                            resize_keyboard=True, 
                            input_field_placeholder="Выбери пункт меню")

game_help = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Морской бой")]])

continue_pair_req = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да, продолжить', callback_data = 'cntue_pair_req'),
                                                   InlineKeyboardButton(text='Не, пусть будут', callback_data = 'un_cntue_pair_req')]])

pair_y_or_n = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да 🫂', callback_data='pairyes'),
                                                     InlineKeyboardButton(text='Нет ✋', callback_data='pairno')]]) #создать пару с тем-то тем-то?

cancel_pair_req = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отменить', callback_data = 'cancel_create_pail_req')]]) #перестать писать id пользователя?

test = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = '🤨 Узнать id 🧐', copy_text=CopyTextButton(text='🤨 Узнать id 🧐'))]])

game_y_or_n = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Даа, погна!", callback_data="game_yes"),
                                                     InlineKeyboardButton(text="Не, чёта не хочу пока", callback_data="game_no")]])