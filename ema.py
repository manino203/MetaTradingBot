from datetime import datetime

import MetaTrader5 as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta



symbol = "XAUUSD"
mt.initialize()
# timezone = pytz.timezone("EET")

values = mt.copy_rates_range(
    symbol,
    mt.TIMEFRAME_M5,
    datetime.now() - relativedelta(hours=24),
    datetime.now()
)

df = pd.DataFrame(values)

span1 = 9
span2 = 21


df["EMA_fast"] = df['close'].ewm(alpha=2 / (span1 + 1), adjust=False).mean()

# Create Simple moving average 60 days
df["EMA_slow"] = df['close'].ewm(alpha=2 / (span2 + 1), adjust=False).mean()


df["signal"] = np.nan

# Create the condition
# condition_buy = (df["EMA_fast"] > df["EMA_slow"]) & (df["EMA_fast"].shift(1) < df["EMA_slow"].shift(1))
condition_buy = (df["EMA_fast"].shift(1) > df["EMA_slow"].shift(1)) & (df["EMA_fast"].shift(2) < df["EMA_slow"].shift(2)) & (df['close'] > df['open'])
# condition_sell = (df["EMA_fast"] < df["EMA_slow"]) & (df["EMA_fast"].shift(1) > df["EMA_slow"].shift(1))
condition_sell = (df["EMA_fast"].shift(1) < df["EMA_slow"].shift(1)) & (df["EMA_fast"].shift(2) > df["EMA_slow"].shift(2)) & (df['open'] > df['close'])

df.loc[condition_buy, "signal"] = 1
df.loc[condition_sell, "signal"] = -1

# Select all signal in a index list to plot only this points
idx_open = df.loc[df["signal"] == 1].index
idx_close = df.loc[df["signal"] == -1].index

# Adapt the size of the graph
# plt.figure(figsize=(30, 12))

# Plot the points of the open long signal in green and sell in red


# Plot the resistance to be sure that the conditions are completed

# Separate up and down movements
up = df[df.close >= df.open]
down = df[df.close < df.open]

# Plotting parameters
width = 0.7
width2 = 0.1

# Plot up prices
plt.bar(up.index, up.close - up.open, width, bottom=up.open, color='green')
plt.bar(up.index, up.high - up.close, width2, bottom=up.close, color='green')
plt.bar(up.index, up.low - up.open, width2, bottom=up.open, color='green')

# Plot down prices
plt.bar(down.index, down.close - down.open, width, bottom=down.open, color='red')
plt.bar(down.index, down.high - down.open, width2, bottom=down.open, color='red')
plt.bar(down.index, down.low - down.close, width2, bottom=down.close, color='red')

# Rotate x-axis tick labels
plt.xticks(rotation=45, ha='right')

# Display the candlestick chart
plt.title('Stock Prices for a Week')
plt.xlabel('Date')
plt.ylabel('Price (USD)')



plt.plot(df["close"].index, df["EMA_fast"], alpha=0.35)

plt.plot(df["close"].index, df["EMA_slow"], alpha=0.35)

plt.legend(["Buy", "Sell", "symbol"])
plt.scatter(idx_open, df.loc[idx_open]["close"], color="blue", marker="^", s=50)
plt.scatter(idx_close, df.loc[idx_close]["close"], c="orange", marker="v", s=50)

plt.show()


