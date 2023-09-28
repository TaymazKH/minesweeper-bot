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
        c1 = 5 <= width <= 8
        c2 = 5 <= height <= 11
        c3 = width * height <= 95
        c4 = 7 <= mines <= width * height
        c5 = mines % 2 == 1
        if c1 and c2 and c3 and c4 and c5:
            title = 'Start Game'
            text = messages.LETS_PLAY
            markup = InlineKeyboardMarkup.from_button(InlineKeyboardButton(
                "Let's play!",
                callback_data=f's {height} {width} {mines} {update.inline_query.from_user.id}'
            ))
        else:
            f = lambda c: '✅' if c else '❌'
            title = 'Invalid Query'
            text = messages.INVALID_INLINE_ARGS.format(c1=f(c1), c2=f(c2), c3=f(c3), c4=f(c4), c5=f(c5))
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
    raw_data = update.callback_query.data
    if raw_data[0] not in ('s', 'm'):
        await update.callback_query.answer()
        return

    data = [int(i) for i in raw_data.split()[1:]]
    data.insert(0, {'s': 0, 'm': 1}[raw_data[0]])
    userid = update.callback_query.from_user.id

    if data[0] == 0:
        if data[4] == userid:
            await update.callback_query.answer(text=messages.CANT_PLAY_WITH_YOURSELF, show_alert=True)
        else:
            table, visit = game.generate_map(data[1], data[2], data[3])
            text = messages.GAME
            markup = functions.get_game_markup(table, visit, (data[4], userid), 1)
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text, reply_markup=markup)
    elif data[0] == 1:
        game_state = functions.get_game_state(update.message.reply_markup)
        if game_state['players'][game_state['turn'] - 1] != userid:
            await update.callback_query.answer(text=messages.NOT_YOUR_TURN, show_alert=True)
        else:
            table = game_state['table']
            visit = game_state['visit']
            turn = game_state['turn']
            win, changed, turn = game.move(table, visit, data[1], data[2], turn)
            if win:
                text = messages.WIN
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(text)
            elif changed:
                text = messages.GAME
                markup = functions.get_game_markup(table, visit, game_state['players'], turn)
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(text, reply_markup=markup)
            else:
                await update.callback_query.answer(text=messages.ALREADY_REVEALED, show_alert=True)
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(messages.UNKNOWN_ERROR)


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
