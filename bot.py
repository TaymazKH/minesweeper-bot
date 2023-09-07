import json
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, \
    filters, Defaults, CallbackContext

import functions
import game
import messages


async def handle_start(update: Update, context: CallbackContext):
    await context.bot.send_message(
        update.message.from_user.id,
        messages.START.format(bot_name=context.bot.bot.full_name, bot_username=context.bot.username)
    )


async def handle_inline(update: Update, context: CallbackContext):
    query = update.inline_query.query
    try:
        if query:
            height, width, mines = [int(i) for i in query.split()]
        else:
            height, width, mines = 8, 8, 21
        c1 = width <= 8
        c2 = width * height <= 100
        c3 = width * height >= mines
        c4 = mines % 2 == 1
        if c1 and c2 and c3 and c4:
            keyboard = [[InlineKeyboardButton(
                "Let's play!",
                callback_data=json.dumps(
                    {'operation': 'start_game', 'player': update.inline_query.from_user.id, 'height': height,
                     'width': width, 'mines': mines})
            )]]
            title = 'Start Game'
            text = messages.LETS_PLAY
            markup = InlineKeyboardMarkup(keyboard)
        else:
            title = 'Invalid Query'
            text = messages.INVALID_INLINE_ARGS.format(
                c1='✅' if c1 else '❌', c2='✅' if c2 else '❌', c3='✅' if c3 else '❌', c4='✅' if c4 else '❌')
            markup = None
    except ValueError:
        title = 'Invalid Query'
        text = messages.INVALID_INLINE_FORMAT.format(
            bot_name=context.bot.bot.full_name, bot_username=context.bot.username)
        markup = None
    results = [InlineQueryResultArticle(
        id='0',
        title=title,
        input_message_content=InputTextMessageContent(text),
        reply_markup=markup
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def handle_callback(update: Update, context: CallbackContext):
    data = json.loads(update.callback_query.data)
    userid = update.callback_query.from_user.id

    if data['operation'] == 'start_game':
        if data['player'] == userid:
            await update.callback_query.answer(text=messages.CANT_PLAY_WITH_YOURSELF, show_alert=True)
        else:
            table, visit = game.generate_map(data['height'], data['width'], data['mines'])
            text = messages.GAME
            markup = functions.get_game_markup(table, visit, (data['player'], userid), 1)
            await update.callback_query.answer()
            await update.callback_query.message.edit_text(text, reply_markup=markup)
    elif data['operation'] == 'move':
        if data['players'][data['turn'] - 1] != userid:
            await update.callback_query.answer(text=messages.NOT_YOUR_TURN, show_alert=True)
        else:
            table = data['table']
            visit = data['visit']
            turn = data['turn']
            changed, turn = game.move(table, visit, data['x'], data['y'], turn)
            if changed:
                text = messages.GAME
                markup = functions.get_game_markup(table, visit, data['players'], turn)
                await update.callback_query.answer()
                await update.callback_query.message.edit_text(text, reply_markup=markup)
            else:
                await update.callback_query.answer(text=messages.NO_CHANGE, show_alert=True)
    else:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(messages.UNKNOWN_ERROR)


async def handle_chat(update: Update, context: CallbackContext):
    pass


def run():
    load_dotenv()
    token = os.getenv('TOKEN')
    defaults = Defaults(parse_mode=ParseMode.HTML)
    application = ApplicationBuilder().token(token).defaults(defaults).build()
    application.add_handler(CommandHandler('start', handle_start))
    application.add_handler(InlineQueryHandler(handle_inline))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.ALL, handle_chat))
    application.run_polling()


if __name__ == '__main__':
    run()
