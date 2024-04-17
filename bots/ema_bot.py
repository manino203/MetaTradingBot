import asyncio
from datetime import datetime

import numpy as np
from dateutil.relativedelta import relativedelta

import MetaTrader5 as mt5

from metatrader.mt5_layer import Mt5Layer
from metatrader.timeframe import TIMEFRAME_M5


class EmaBot:

    def __init__(self, symbol, timezone):
        self.timezone = timezone
        self.symbol = symbol
        self.trader = Mt5Layer()
        self.info = "EmaBot"
        self.span_faster = 9

        self.span_slower = 21
        self.timeframe = TIMEFRAME_M5
        self.volume = 1

    def close_positions(self):
        for pos in self.trader.get_open_positions(self.symbol):
            if pos.profit >= 100 or pos.profit <= -50:
                self.trader.close_position(pos)

    async def open_loop(self):

        while True:
            df = self.trader.get_data(
                self.symbol,
                self.timeframe.mt_timeframe,
                datetime.now() - relativedelta(weeks=1),
                datetime.now()
            )
            df["EMA_fast"] = df['close'].ewm(alpha=2 / (self.span_faster + 1), adjust=False).mean()

            df["EMA_slow"] = df['close'].ewm(alpha=2 / (self.span_slower + 1), adjust=False).mean()

            df["signal"] = np.nan

            condition_buy = (df["EMA_fast"].shift(1) > df["EMA_slow"].shift(1)) & (
                    df["EMA_fast"].shift(2) < df["EMA_slow"].shift(2)) & (df['close'] > df['open'])
            condition_sell = (df["EMA_fast"].shift(1) < df["EMA_slow"].shift(1)) & (
                    df["EMA_fast"].shift(2) > df["EMA_slow"].shift(2)) & (df['open'] > df['close'])

            df.loc[condition_buy, "signal"] = 1
            df.loc[condition_sell, "signal"] = -1
            # todo: calc volume
            if df['signal'].iloc[-1] == 1:
                self.trader.open_buy_position(self.symbol, self.volume, self.info)
            elif df['signal'].iloc[-1] == -1:
                self.trader.open_sell_position(self.symbol, self.volume, self.info)

            await asyncio.sleep(self.timeframe.seconds)

    async def close_loop(self):
        while True:
            self.close_positions()
            await asyncio.sleep(0.1)

    def start(self):

        async def main():
            # wait for current candle to close before starting
            await asyncio.sleep(self.timeframe.seconds - (datetime.now().timestamp() % self.timeframe.seconds))
            task1 = asyncio.create_task(self.open_loop())
            task2 = asyncio.create_task(self.close_loop())

            await task1
            await task2

        self.trader.mt_auth()
        print(f"started: {self.info}")
        asyncio.run(main())
