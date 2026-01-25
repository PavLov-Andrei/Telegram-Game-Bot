import asyncio
import logging
import threading

from aiogram import Bot, Dispatcher
from app.handlers import router
from app.FSM_handlers import fsmrouter
from source.source import *
dp = Dispatcher()


async def main():
    dp.include_router(fsmrouter)
    dp.include_router(router)
    #blyat_otkuda_zdess_pcholyy = asyncio.create_task(expired_pchol())
    start_bot = asyncio.create_task(dp.start_polling(bot))
    await start_bot
    #await blyat_otkuda_zdess_pcholyy


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit with 0") 
##1192484415 яяяяя
###Стааасенькьаааа     1558359426 <--- Основа
####     6513499701 <--- Второц нянмнямнямюбююбпуаиа