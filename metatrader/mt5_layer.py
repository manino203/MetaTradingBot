from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from dateutil.relativedelta import relativedelta

from auth_data import *
from log.logger import Logger


# noinspection PyMethodMayBeStatic
class Mt5Layer:

    def __init__(self):
        self.logger = Logger()

    def mt_auth(self):
        if not mt5.initialize():
            print("Failed to initialize MetaTrader5!")
            self.quit()
        if not mt5.login(login, password, server):
            print("Failed to login to MetaTrader5!")
            self.quit()
        print("MetaTrader init successful!")

    # noinspection PyMethodMayBeStatic
    def execute_order(self, request):
        order = mt5.order_send(request)
        if order:
            self.logger.log("ORDER SENT")
        else:
            self.logger.log("ORDER FAILED")
            self.logger.log(f"{mt5.last_error()}")

    def get_data(self, symbol, timeframe, date_from, date_to):
        return pd.DataFrame(mt5.copy_rates_range(symbol, timeframe, date_from, date_to))

    def is_position_for_symbol_open(self, symbol):
        return list(filter(lambda x: x.symbol == symbol, mt5.positions_get())) != []

    def curr_symbol_info(self, symbol):
        return mt5.symbol_info_tick(symbol)

    def close_position(self, position):
        if position.type == mt5.ORDER_TYPE_BUY:
            self.open_sell_position(
                position.symbol,
                position.volume,
                "",
                position.ticket
            )
        else:
            self.open_buy_position(
                position.symbol,
                position.volume,
                "",
                position.ticket
            )

    def get_open_positions(self, symbol):
        return list(filter(lambda x: x.symbol == symbol, mt5.positions_get()))

    def get_position(self, ticket):
        return list(filter(lambda x: x.ticket == ticket, mt5.positions_get()))[0]

    def open_sell_position(
            self,
            symbol,
            volume,
            bot_info,
            position=None,
            sl=0.0,
            tp=0.0,
            deviation=20,
            magic=234000
    ):
        self.open_position(
            symbol,
            volume,
            mt5.ORDER_TYPE_SELL,
            bot_info,
            sl=sl,
            tp=tp,
            position=position,
            deviation=deviation,
            magic=magic
        )

    def open_buy_position(
            self,
            symbol,
            volume,
            bot_info,
            position=None,
            sl=0.0,
            tp=0.0,
            deviation=20,
            magic=234000
    ):
        self.open_position(
            symbol,
            volume,
            mt5.ORDER_TYPE_BUY,
            bot_info,
            sl=sl,
            tp=tp,
            position=position,
            deviation=deviation,
            magic=magic
        )

    def open_position(
            self,
            symbol,
            volume,
            order_type,
            bot_info,
            position=None,
            sl=0.0,
            tp=0.0,
            action=mt5.TRADE_ACTION_DEAL,
            deviation=20,
            magic=234000,
            type_time=mt5.ORDER_TIME_GTC,
            type_filling=mt5.ORDER_FILLING_IOC,
    ):
        request = {
            "action": action,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": mt5.symbol_info_tick(symbol).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(
                symbol).ask,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "comment": f"Opened by: {bot_info}",
            "type_time": type_time,
            "type_filling": type_filling,
        }
        if position:
            self.logger.log_close(self.get_position(position))
            request["position"] = position
        else:
            self.logger.log_open(request)
        self.execute_order(request)

    def get_current_balance(self):
        return mt5.account_info().balance

    def quit(self):
        print(",error code =", mt5.last_error())
        mt5.shutdown()
        quit()
