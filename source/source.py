from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TOKEN

import asyncio
import json

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

pair_requests = {} #запросы пользователей на составление пар

def find_pair(user_id: int) -> int:
       user_id = str(user_id)
       with open('source/source.json', 'r', encoding = 'utf-8') as file:
              data = json.load(file)
       if user_id in data["users_pairs"]:
              return int(data["users_pairs"][user_id])
       for first_user in data["users_pairs"]:
              if data["users_pairs"][first_user] == user_id:
                     return int(first_user)
       return 0

def create_pair(first_user: str, second_user: str) -> None:
       with open('source/source.json', 'r', encoding = 'utf-8') as file:
              data = json.load(file)
       data["users_pairs"][first_user] = second_user
       with open('source/source.json', 'w', encoding = 'utf-8') as file:
              json.dump(data, file, indent=4)

def delete_pair(user_id: int) -> int: #удаляет пару, в случае успеха возвращает id второго пользвателя,
                                      #иначе - 0
       with open('source/source.json', 'r', encoding = 'utf-8') as file:
              data = json.load(file)
       user_id = str(user_id)
       second_user = 0
       if user_id in data["users_pairs"]:
              second_user = int(data["users_pairs"][user_id])
              del data["users_pairs"][user_id]
       else:
              for first_user in data["users_pairs"]: #именно отдельная переменная, т.к. значение 0 будет меняться в цикле
                     if data["users_pairs"][first_user] == user_id:
                            second_user = int(first_user)
                            del data["users_pairs"][first_user]
                            break
       if second_user != 0:
              with open('source/source.json', 'w', encoding = 'utf-8') as file:
                     json.dump(data, file, indent=4)

       return second_user #если успешно удалили, возвращаем id второго пользователя, иначе - возвращаем 0