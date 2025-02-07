from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from get_crypto_price import get_crypto_price
from subscribe import Subscribe
from dotenv import load_dotenv
import nest_asyncio
import asyncio
import os

load_dotenv()
nest_asyncio.apply()

TOKEN = os.getenv("TOKEN")

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('You can use "/check" to check if the bot is up and running.\n'
                                    'You can use "/price {cryptoName}" to check the price.\n'
                                    'You can use "/subscribe {cryptoName} {percent}" to get notified when the price rises or falls.\n'
                                    'You can use "/unsubscribe {cryptoName} {percent}" turn the /subscribe command off.\n')

async def check(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('The bot is up and running.')

async def price(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1:
        crypto = context.args[0]
        price = get_crypto_price(crypto)
        await update.message.reply_text('Something went wrong; Please try again' if price == -1 else f'The {crypto} price is {price} USD.')
    else:
        await update.message.reply_text('The command is not valid; Please try again.')

async def subscribe(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 2:
        await update.message.reply_text('The bot will send you a message when the price is updated.')
        subscribes.append(Subscribe(context.args[0], context.args[1], update))
    else:
        await update.message.reply_text('The command is not valid; Please try again.')

async def handle_subscribes() -> None:
    while True:
        for sub in subscribes:
            await sub.subscribe()
        await asyncio.sleep(10)

async def unsubscribe(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 2:
        unsub = Subscribe(context.args[0], context.args[1], update)
        if unsub in subscribes:
            subscribes.pop(subscribes.index(unsub))
            await update.message.reply_text('The unsubscribe was successful.')
        else:
            await update.message.reply_text('There is no subscribe like this.')
    else:
        await update.message.reply_text('The command is not valid; Please try again.')

subscribes = []

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    task = [asyncio.create_task(handle_subscribes()), asyncio.create_task(application.run_polling())]
    await task[0]
    await task[1]

if __name__ == "__main__":
    asyncio.run(main())