from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import requests
import asyncio
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

async def check_subscribe(crypto: str, changePercent: float, update: Update) -> None:
    initPrice = -1
    while initPrice == -1:
        initPrice = get_crypto_price(crypto)
    while True:
        newPrice = get_crypto_price(crypto)
        if initPrice * (1 + changePercent / 100) == newPrice:
            await update.message.reply_text(f'The {crypto} price has changed to {newPrice} USD now.')
            return
        await asyncio.sleep(3)

async def subscribe(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 2:
        await update.message.reply_text('The bot will send you a message when the price is updated.')
        asyncio.create_task(check_subscribe(context.args[0], float(context.args[1]), update))
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