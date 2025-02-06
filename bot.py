from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('The bot is up and running.')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    main()