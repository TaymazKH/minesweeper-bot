import os

from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, \
    filters, CallbackContext

import messages


async def handle_start(update: Update, context: CallbackContext):
    pass


async def handle_inline(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    try:
        height, width, mines = [int(i) for i in query.split()]
        c1 = width <= 8
        c2 = width * height <= 100
        c3 = width * height >= mines
        c4 = mines % 2 == 1
        if c1 and c2 and c3 and c4:
            pass
        else:
            results = [InlineQueryResultArticle(
                id='0',
                title='Invalid Query',
                input_message_content=InputTextMessageContent(messages.INVALID_INLINE_ARGS)
            )]
    except ValueError:
        results = [InlineQueryResultArticle(
            id='0',
            title='Invalid Query',
            input_message_content=InputTextMessageContent(messages.INVALID_INLINE_FORMAT)
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
