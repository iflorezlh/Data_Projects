import pandas as pd
import yfinance as yf


# ticker = yf.Ticker("MSFT")
# print(pd.json_normalize(ticker.info))

ticker = 'WEX'
df = pd.DataFrame([[ticker]], columns=['Ticker'])
print(df)