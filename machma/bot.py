from aiogram import Bot, Dispatcher, executor, types
import logging
import pprint

from .db import BotDB

API_TOKEN = open('./api_token.txt', 'r').read()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
bot_db = BotDB('./bot.db')

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("I won't help you.")

@dp.message_handler(commands=['exercise', 'übung'])
async def add_exercise(message: types.Message):
    args = message.get_args().strip().split(' ')

    if len(args) < 1:
        await message.answer('Zu wenig Argumente, du Otto.')
    elif len(args) > 2:
        await message.answer('Zu viele Argumente, du Otto.')
    else:
        exercise = args[0]
        logging.info(exercise)
        if bot_db.has_exercise(exercise):
            await message.answer('Diese Übung gibt es bereits.')
        else:
            link = args[1] if len(args) > 1 else None
            bot_db.add_exercise(exercise, link=link)

@dp.message_handler(commands=['alias'])
async def add_alias(message: types.Message):
    args = message.get_args().strip.split(' ')

    if len(args) < 2:
        await message.answer('Zu wenig Argumente, du Otto.')
    elif len(args) > 2:
        await message.answer('Zu viele Argumente, du Otto.')
    else:
        alias, exercise = args
        if bot_db.has_alias(exercise):
            await messsage.answer('Dieser Alias existiert bereits.')
        else:
            bot_db.add_alias(alias, exercise)
            await message.answer('{} oder {}? Alles das gleiche!'.format(alias, exercise))


@dp.message_handler(commands=['machma', 'getan', 'done'])
async def send_help(message: types.Message):
    args = message.get_args().strip().split(' ')

    if len(args) < 2:
        await message.answer('Zu wenig Argumente, du Otto.')
    elif len(args) > 2:
        await message.answer('Zu viele Argumente, du Otto.')
    else:
        try:
            exercise = args[1]
            reps = int(args[0])
            from_user = message['from']
            if not bot_db.has_user(from_user['id']):
                bot_db.add_user(from_user['id'], from_user['username'], from_user['first_name'], from_user['last_name'])
            if not bot_db.has_exercise(exercise):
                await message.answer('Die Übung existiert nicht.')
            else:
                bot_db.add_to_user_reps(from_user['id'], exercise, reps)
                await message.answer('Du hast {} {} gemacht'.format(reps, exercise))
        except ValueError:
            await message.answer('Ne Zahl! Ist das so schwer?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
