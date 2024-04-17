import asyncio
from auth_data import *
import MetaTrader5 as mt
import pandas as pd

from bots.ema_bot import EmaBot
from log.logger import Logger

if __name__ == "__main__":
    tz = "EET"
    Logger(tz)
    EmaBot("XAUUSD", tz).start()

