from telegram import Update
from get_crypto_price import get_crypto_price

class Subscribe:
    crypto: str
    changePercent: float
    update: Update
    initPrice: float

    def __init__(self, crypto: str, changePercent: float, update: Update):
        self.crypto = crypto
        self.changePercent = float(changePercent)
        self.update = update
        self.initPrice = get_crypto_price(crypto)

    def check_subscribe(self):
        while True:
            newPrice = get_crypto_price(self.crypto)
            if self.initPrice * (100 + self.changePercent) == newPrice:
                self.update.message.reply_text(f'The new price is {newPrice} USD.')
                del self
                return


