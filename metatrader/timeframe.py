import MetaTrader5 as mt5


class TimeFrame:

    def __init__(self, mt_timeframe, seconds):
        self.mt_timeframe = mt_timeframe
        self.seconds = seconds


TIMEFRAME_M1 = TimeFrame(mt5.TIMEFRAME_M1, 1 * 60)
TIMEFRAME_M2 = TimeFrame(mt5.TIMEFRAME_M2, 2 * 60)
TIMEFRAME_M3 = TimeFrame(mt5.TIMEFRAME_M3, 3 * 60)
TIMEFRAME_M4 = TimeFrame(mt5.TIMEFRAME_M4, 4 * 60)
TIMEFRAME_M5 = TimeFrame(mt5.TIMEFRAME_M5, 5 * 60)
TIMEFRAME_M6 = TimeFrame(mt5.TIMEFRAME_M6, 6 * 60)
TIMEFRAME_M10 = TimeFrame(mt5.TIMEFRAME_M10, 10 * 60)
TIMEFRAME_M12 = TimeFrame(mt5.TIMEFRAME_M12, 12 * 60)
TIMEFRAME_M15 = TimeFrame(mt5.TIMEFRAME_M15, 15 * 60)
TIMEFRAME_M20 = TimeFrame(mt5.TIMEFRAME_M20, 20 * 60)
TIMEFRAME_M30 = TimeFrame(mt5.TIMEFRAME_M30, 30 * 60)
TIMEFRAME_H1 = TimeFrame(mt5.TIMEFRAME_H1, 1 * 60 * 60)
TIMEFRAME_H2 = TimeFrame(mt5.TIMEFRAME_H2, 2 * 60 * 60)
TIMEFRAME_H4 = TimeFrame(mt5.TIMEFRAME_H4, 4 * 60 * 60)
TIMEFRAME_H3 = TimeFrame(mt5.TIMEFRAME_H3, 3 * 60 * 60)
TIMEFRAME_H6 = TimeFrame(mt5.TIMEFRAME_H6, 6 * 60 * 60)
TIMEFRAME_H8 = TimeFrame(mt5.TIMEFRAME_H8, 8 * 60 * 60)
TIMEFRAME_H12 = TimeFrame(mt5.TIMEFRAME_H12, 12 * 60 * 60)
TIMEFRAME_D1 = TimeFrame(mt5.TIMEFRAME_D1, 1 * 60 * 60 * 24)
TIMEFRAME_W1 = TimeFrame(mt5.TIMEFRAME_W1, 1 * 60 * 60 * 24 * 7)
