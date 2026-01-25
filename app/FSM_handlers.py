from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from random import randint
from source.source import *
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from app.handlers import Some_State
from aiogram.exceptions import (TelegramBadRequest, TelegramForbiddenError, TelegramNotFound)
#from PIL import Image

import time
import app.keyboards as kb
import asyncio


fsmrouter = Router()

@fsmrouter.message(Some_State.write_id)
async def fsm_pair_request(message: Message, state: FSMContext, bot: Bot):
    if not(message.text.isdigit()) or (len(message.text) != 10):
        await message.answer("Это не id пользователя! Пожалуйста, напиши либо id пользоателя, с которым хочешь составить пару, либо отмени отправку запроса", reply_markup = kb.cancel_pair_req)
    elif message.text in pair_requests and pair_requests[message.text] != str(message.chat.id):
        await message.answer("*Этот пользователь уже ждёт ответа от кого-то :(*\n\nТы можешь написать id другого пользователя или вообще отменить отправку запроса", reply_markup = kb.cancel_pair_req)
    elif find_pair(int(message.text)):
        await message.answer("*У этого пользователя уже есть пара :(*\n\nТы можешь написать id другого пользователя или вообще отменить отправку запроса", reply_markup = kb.cancel_pair_req)
    else:
        pair_cnt = 0
        for user in pair_requests:
            if pair_requests[user] == str(message.chat.id): #если кто-то отправлял запос нашему пользователю
                if user != message.text: #а то вдруг два гения каких-то друг дугу заявку кинут
                    pair_cnt += 1
                    del pair_requests[user]
                    await bot.send_message(int(user), f'Пользователь *{message.chat.id}* отклонил твою заявку на создание пары :(')
                else: 
                    del pair_requests[user] #удаляем запрос тому, которому сейчас сами его кинули
                    for user1 in pair_requests: #удаляем все остальные запросы нам
                        if pair_requests[user1] == str(message.chat.id):
                            del pair_requests[user1]
                            await bot.send_message(int(user1), f'Пользователь *{message.chat.id}* отклонил твою заявку на создание пары :(')
               
                    create_pair(user, str(message.chat.id))
                    await message.answer("Чтож! Вы два гения, отправивших заявки друг другу! Вот это связь! Пара создана!")
                    await bot.send_message("Чтож! Вы два гения, отправивших заявки друг другу! Вот это связь! Пара создана!")
                    return        
        try:
            await bot.send_message(int(message.text), f'Пользователь {str(message.chat.id)} отправил Вам запрос на создание пары! Принять его?', reply_markup = kb.pair_y_or_n)        
            pair_requests[str(message.chat.id)] = message.text #если всё чётко осталось, то добавляем новый запрос
        except TelegramBadRequest:
            await message.answer("Такого id не существует, перепроверь, пожалуйста, и напиши ещё раз. Так же ты можешь отменить запрос", reply_markup = kb.pair_y_or_n)
            return
        except TelegramForbiddenError:
            await message.answer("Бот либо заблокирован, либо пользователь не нажал в нём /start. В любом случае, напиши ему лично или отмени запрос на создание пары", reply_markup = kb.pair_y_or_n)
            return
        except TelegramNotFound:
            await message.answer("Хм, не могу найти чат.. Перепроверь id и напиши новый или отмени запрос на создание пары", reply_markup = kb.pair_y_or_n)
            return
        await state.clear()
        if pair_cnt > 0:
            await message.answer(f'Во всех обращениях на создание пары с тобой было отказано, ты выбрал кого-то особенного, ждём когда он/она примет твою заявку! Отказано вот стольким челикам: {pair_cnt}')
        else:
            await message.answer(f'Всё, ты отправил запрос {message.text}! Теперь ждём')
       
@fsmrouter.callback_query(Some_State.write_id, F.data == 'cancel_create_pail_req')
async def cancel_pair_req_fsm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await bot.edit_message_text(text = "Создание пары отменёноооЫЫ", chat_id=callback.message.chat.id, message_id=callback.message.message_id)

#@fsmrouter.message(F.text == ">> 🎲 <<")
#async def test_kubs(message: Message):
 #   await message.answer("Это, конечно, никуда не пойдёт, но...")
  #  await bot.send_dice(message.chat.id, reply_markup=ReplyKeyboardRemove(remove_keybord=True))
