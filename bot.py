import json
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, \
    filters, CallbackContext

import messages


async def handle_start(update: Update, context: CallbackContext):
    pass


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
            text = messages.INVALID_INLINE_ARGS
            markup = None
    except ValueError:
        title = 'Invalid Query'
        text = messages.INVALID_INLINE_FORMAT
        markup = None
    results = [InlineQueryResultArticle(
        id='0',
        title=title,
        input_message_content=InputTextMessageContent(text),
        reply_markup=markup
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def handle_callback(update: Update, context: CallbackContext):
    pass


async def handle_chat(update: Update, context: CallbackContext):
    pass


def run():
    load_dotenv()
    token = os.getenv('TOKEN')
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', handle_start))
    application.add_handler(InlineQueryHandler(handle_inline))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.ALL, handle_chat))
    application.run_polling()


if __name__ == '__main__':
    run()
