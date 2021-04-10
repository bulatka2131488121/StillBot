import logging
import asyncio
from datetime import datetime
import os.path

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token='1645152567:AAHfc_DhZDuOn3-iloEI1UbfF78Z8yNjoAU')
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# file_path = "C:\Users\admin\Desktop\StillBot-main"
###filess = os.path.exists(file_path)
# Команда активации подписки


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")

# Команда отписки


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")

# проверяем наличие новых игр и делаем рассылки


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

    subscriptions = db.get_subscriptions()

    with open('text.txt', 'rb') as file:
        for s in subscriptions:
            await bot.send_document(message.from_user.id, file)
            await bot.send_document(message.from_user.id, "FILEID")



if __name__ == '__main__':
    ##dp.loop.create_task(scheduled(10)) # пока что оставим 10 секунд (в качестве теста)
    executor.start_polling(dp, skip_updates=True)
