import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = open('./api_token.txt', 'r').read()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("I won't help you.")

numbers = [10, 15, 20, 30]
@dp.callback_query_handler(lambda cb: True)
async def inline_kb_callback_handler(query: types.CallbackQuery):
    await query.answer()

    count = query.data
    await bot.send_message(query.from_user.id, count)

@dp.message_handler(commands=['machma', 'getan', 'done'])
async def send_help(message: types.Message):
    args = message.get_args().strip().split(' ')

    async def suggest_count(text):
        keyboard_markup = types.InlineKeyboardMarkup(row_width=len(numbers))
        keyboard_markup.row(*[types.InlineKeyboardMarkup(text=str(i), callback_data=i) for i in numbers])

        await message.reply(text, reply_markup=keyboard_markup)

    if len(args) > 2:
        await message.answer('Zu viele Argumente, du Otto.')
    else:
        exercise = args[0]
        if len(args) == 1:
            await suggest_count('Ich brauch ne Zahl, hier sind ein paar Vorschläge')
        else:
            try:
                count = int(args[1])
                await message.answer('Du hast die Übung {} {}-mal gemacht.'.format(exercise, count))
            except:
                await suggest_count('Ne Zahl, du Otto. Hier sind ein paar Beispiele')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
