from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import requests
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('The bot is up and running.')

def get_crypto_price(crypto: str) -> float:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[crypto]["usd"]
    else:
        return -1;

async def get_price(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1:
        crypto = context.args[0]
        price = get_crypto_price(crypto)
        await update.message.reply_text('The crypto name is not valid; Please try again' if price == -1 else f'The {crypto} price is {price} USD.')
    else:
        await update.message.reply_text('The command is not valid; Please try again.')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_price", get_price))
    application.run_polling()

if __name__ == "__main__":
    main()