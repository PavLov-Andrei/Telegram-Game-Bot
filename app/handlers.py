from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from random import randint
from source.source import *
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
#from PIL import Image 

import app.keyboards as kb

router = Router()

class Kubs(StatesGroup):
    pchol = State()
    wait_pchol = State()

class Some_State(StatesGroup):
    write_id = State()
    write_id_to_pair_accept = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Приветик! Этот бот создан специальненько для нас, чтобы мы были рядышком даже на большом расстоянии, ня <3')
    print(message.from_user.id)

@router.message(Command('help'))
async def cmd_help(message: Message, bot: Bot):
    await message.answer('Йоу! Вот команды, которыми ты можешь пользоваться с моей помощью!', reply_markup=kb.help)
    #await bot.send_sticker(message.from_user.id, help_stikers[randint(0, len(help_stikers)-1)])

@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer('Выбери команду, про которую хочешь узнать попотробнее', reply_markup=kb.info)

@router.message(F.text == "Админское")
async def admin_help(message: Message):
    await message.answer('Йоу! Вот команды для создание и редактирования твоей пары!', reply_markup=kb.admin_help)

@router.message(F.text == "Игровоевое")
async def game_help(message: Message):
    await message.answer('Йоу! Вот все игры, в которые ты можешь пограть со своей парой!', reply_markup=kb.game_help)

@router.message(F.text == '🤨 Узнать id 🧐')
async def send_user_id(message: Message):
    await message.answer(f'*Вот твой id!*\n`{message.chat.id}`')

@router.message(F.text == "💃 Создать пару 🕺")
async def favorite(message: Message, state: FSMContext):
    second_user = find_pair(message.chat.id)
    if second_user:
        await message.answer(f'У тебя уже есть пара с пользователем *{second_user}*! Если хочешь поменять партнёра, напиши в чат *"Я МЕНЯЮ ПАРУ"*')
    elif str(message.chat.id) in pair_requests:
        await message.answer(f'Ты уже отправлял запрос на создание пары с *{pair_requests[str(message.chat.id)]}*! Если хочешь отправить новый, то отмени этот, вот кнопки с командами!', reply_markup = kb.admin_help)
    else:
        a = [x for x in pair_requests if pair_requests[x] == str(message.chat.id)]
        if len(a) > 0:
            await message.answer(f'Если ты отправишь кому-то запрос на составление пары, ты автоматически отклонишь все запросы тебе (а их *{len(a)})*\nПродолжить?\n\n', reply_markup = kb.continue_pair_req)
        else:
            await state.set_state(Some_State.write_id)
            await message.answer("Отлично! Теперь скинь id того пользователя, с которым хочешь составить пару!")

@router.callback_query(F.data == "pairyes") #кнопка "согласиться создать пару"
async def pairyes(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    from_user = callback.message.text[13:23:] #берём из текста сообщения id пользователя
    if find_pair(callback.message.chat.id):     
        await bot.edit_message_text(text = "Бро, у тебя уже создана пара, не недо так отвечать", chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    elif (from_user not in pair_requests) or (pair_requests[from_user] != str(callback.message.chat.id)):
        await bot.edit_message_text(text = "Увы, этот пользователь отозвал свой запрос :(", chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    else:
        del pair_requests[from_user] #удаляем исходный запрос к нам
        create_pair(from_user, str(callback.message.chat.id)) #соглашаемся
        for user in pair_requests: #удаляем все остальные запросы к нам
            if pair_requests[user] == str(callback.message.chat.id) or pair_requests[user] == from_user:
                await bot.send_message(int(user), f'Пользователь *{pair_requests[user]}* отклонил твою заявку на создание пары :(')
                del pair_requests[user]
        
        await bot.send_message(int(from_user), f'Успех! Пользователь *{callback.message.chat.id}* принял твой запрос на состалвение пары')
        await bot.edit_message_text(text = f"Успех! У тебя создана пара с *{from_user}*", chat_id=callback.message.chat.id, message_id=callback.message.message_id)

@router.callback_query(F.data == "pairno") #кнопка "отказаться от создания пары" когда пришло предложение
async def pairno(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    from_user = callback.message.text[13:23:] #берём из текста сообщения id пользователя
    if (from_user not in pair_requests) or (pair_requests[from_user] != str(callback.message.chat.id)):
        await bot.edit_message_text(text = f"Этого запроса уже и нет, йоу!", chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    #тут не надо проверять, есть ли у тебя пара. Если ты только что создал пару, этому пользователю сразу отказали,
    #и его запроса уже нет, а если пара у тебя давно, то он и не мог отправить тебе запрос
    else:
        del pair_requests[from_user] #удаляем запрос от того челика
        await bot.send_message(int(from_user), f'Пользователь *{callback.message.chat.id}* отказал тебе в запросе на создание пары!')
        await bot.edit_message_text(text = f"В запросе на создание пары отказано!", chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        
@router.callback_query(F.data == 'cancel_create_pail_req') #отказаться вводить id пользователя
async def cancel_pair_req(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await bot.edit_message_text(text = "Ты сейчас не находишься в меню ввода id пользователя. Для отмены запроса есть отдельная команда в списке администратинвых команд", chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=kb.admin_help)

@router.message(F.text == "Убрать пару(")
async def start_del_pair(message: Message):
    if not(find_pair(message.chat.id)):
        await message.answer("У тебя пока что нет пары..")
    else:
        await message.answer('Чтобы удалить текущую пару, напиши в чат *"Я МЕНЯЮ ПАРУ"*')

@router.message(F.text == "Отменить запрос")
async def cancel_сreate_pair(message: Message):
    if str(message.chat.id) not in pair_requests:
        await message.answer("У тебя нет активных запросов на создание пары(")
    else:
        del pair_requests[str(message.chat.id)]
        await message.answer("Запрос на создание пары отменён!")

@router.message(F.text == "Я МЕНЯЮ ПАРУ")
async def user_delete_pair(message: Message, bot: Bot):
    second_user = delete_pair(message.chat.id)
    if second_user == 0:
        await message.answer("Бро, у тебя нету пары в этом боте :(")
    else:
        await message.answer("Пара удалена! Пока-Пока!")
        await bot.send_message(second_user, f'Пользователь *{str(message.chat.id)}* решил удалить вашу пару! Пока-пока!')

@router.message(F.text == "❓ Мои запросы ❓")
async def my_requstsions(message: Message, state: FSMContext):
    #если у челика есть пара, то запросов у него их нет
    s = ''
    for user in pair_requests:
        if pair_requests[user] == str(message.chat.id):
            s += f"{s.count('.') + 1}. '{user}'\n"
    if s == '':
        await message.answer("*❗ Твои, твои ❗*\nК тебе пока нет запросов на создание пары :(")
    else:
        await state.set_state(Some_State.write_id_to_pair_accept)
        await message.answer(f'*❗ Твои, твои ❗*\n{s}\nТеперь напиши id того пользователя, чей запрос хочешь принять! Ну, или отмени это', reply_markup=kb.cancel_pair_req)

async def init_game(message: Message, bot: Bot): #чтобы не копировать код в 5 строк в каждую игру
    second_user = find_pair(message.chat.id)
    if not(second_user):
        await message.answer("Увы, у тебя нет пары, поэтому ты не сможишь играц((")
    else:
        create_game(message.chat.id, second_user, message.text)
        await bot.send_message(second_user, f'Твой напарник предложил поиграть в *«{message.text}»*!')

@router.message(F.text == "Морской бой")
async def sea_buttle(message: Message, bot: Bot):
    game = asyncio.create_task(init_game(message, bot))
    await game


"""
@router.message(F.photo)
"""