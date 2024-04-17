from datetime import datetime

import MetaTrader5 as mt5

import pytz

from utils.singleton import singleton


@singleton
class Logger:

    def __init__(self, timezone):
        self.timezone = pytz.timezone(timezone)
        self.log_file = "log/log.txt"

    def log(self, text):
        print(f"{text}\n")
        with open(self.log_file, "a") as f:
            f.write(f"{text}\n")

    def get_request_info(self, request):
        return f"""type: {'Buy' if request['type'] == mt5.ORDER_TYPE_BUY else ('Sell' if request['type'] == mt5.ORDER_TYPE_SELL else '?')}
        volume: {request['volume']}
        price: {request['price']}
        comment: {request['comment']}
        datetime: {(datetime.now(self.timezone)).strftime("%d/%m/%Y %H:%M:%S")}\n"""

    def get_position_info(self, position):
        return f"""type: {'Buy' if position.type == mt5.ORDER_TYPE_BUY else ('Sell' if position.type == mt5.ORDER_TYPE_SELL else '?')}
        volume: {position.volume}
        price: {position.price_open}
        comment: {position.comment}
        datetime: {(datetime.now(self.timezone)).strftime("%d/%m/%Y %H:%M:%S")}
        profit: {position.profit}
        \n"""

    def log_open(self, request):
        self.log(f"POSITION OPEN:\n{self.get_request_info(request)}")

    def log_close(self, position):
        self.log(f"POSITION CLOSED:\n{self.get_position_info(position)}")

