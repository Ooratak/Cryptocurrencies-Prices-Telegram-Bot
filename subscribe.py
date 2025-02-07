import asyncio
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

    def __eq__(self, sub: object) -> bool:
        if isinstance(sub, Subscribe):
            return self.crypto == sub.crypto and self.changePercent == sub.changePercent
        return False

    async def subscribe(self) -> None:
        while True:
            newPrice = get_crypto_price(self.crypto)
            if (self.changePercent >= 0 and self.initPrice * (1 + self.changePercent / 100) <= newPrice) or\
                (self.changePercent < 0 and newPrice <= self.initPrice * (1 + self.changePercent / 100)):
                await self.update.message.reply_text(f'The {self.crypto} new price is {newPrice} USD now.')
            await asyncio.sleep(1)


