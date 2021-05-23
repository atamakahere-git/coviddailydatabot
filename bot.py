import os

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from datafetcher import get_latest_data, get_all_data

TOKEN = os.environ.get('TOKEN', None)
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
POOLING = os.environ.get('POOLING', False)


def start(update: Update, context: CallbackContext) -> None:
    """Command handler to send start message"""
    update.message.reply_text(f"Hello {update.effective_user.first_name}, I'm Covid data bot for India only!\n"
                              f"send /yesterday or /latest to receive latest data\n"
                              f"send /all to receive collective data till date\n")


def yesterday(update: Update, context: CallbackContext) -> None:
    msg = get_latest_data()
    if msg:
        update.message.reply_text(msg)
    else:
        update.message.reply_text("Unknown error occurred")


def all_data(update: Update, context: CallbackContext) -> None:
    msg = get_all_data()
    if msg:
        update.message.reply_text(msg)
    else:
        update.message.reply_text("Unknown error occurred")


def vaccine(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Not working right now, will be implemented later!")


def about(update: Update, context: CallbackContext):
    update.message.reply_text("Made by Tanveer Raza\n"
                              "Visit my github : github.com/tanveerraza789")


def main() -> None:
    updater = None
    try:
        updater = Updater(TOKEN)
    except ValueError:
        print("Token is incorrect")
        exit(1)
    # Command handlers
    updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('help', start, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('yesterday', yesterday, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('latest', yesterday, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('all', all_data, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('about', about, run_async=True))
    # Pooling method to test on local machine
    if POOLING:
        updater.start_polling()
    else:
        # webhook method for heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
    updater.idle()


if __name__ == '__main__':
    main()
