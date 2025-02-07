from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import threading
import requests
import asyncio
import time
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('You can use "/check" to check if the bot is up and running.\n'
                                    'You can use "/get_price {cryptoName}" to check the price.\n'
                                    'You can use "/subscribe {cryptoName} {percent}" to get notified when the price rises or falls.\n')

async def check(update: Update, context: CallbackContext) -> None:
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
        await update.message.reply_text('Something went wrong; Please try again' if price == -1 else f'The {crypto} price is {price} USD.')
    else:
        await update.message.reply_text('The command is not valid; Please try again.')

def check_subscribe(crypto: str, changePercent: float, update: Update) -> None:
    initPrice = get_crypto_price(crypto)
    while True:
        newPrice = get_crypto_price(crypto)
        if initPrice * (1 + changePercent / 100) == newPrice:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(update.message.reply_text(f'The {crypto} price is {newPrice} USD now.'))
            return
        time.sleep(2)

async def subscribe(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 2:
        await update.message.reply_text('The bot will send you a message when the price is updated.')
        thread = threading.Thread(target=check_subscribe, args=(context.args[0], float(context.args[1]), update))
        thread.start()
    else:
        await update.message.reply_text('The command is not valid; Please try again.')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("get_price", get_price))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.run_polling()

if __name__ == "__main__":
    main()