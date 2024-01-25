import pandas as pd
from glob import glob
from datetime import datetime
import os


def delete_duplicated_img():
    files = glob("plots/*")
    times = [datetime.fromtimestamp(os.path.getctime(i)) for i in files]
    os.remove(files[0])


def get_data(path):
    df = pd.read_excel(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['quarter'] = pd.PeriodIndex(df.Date, freq='Q')
    gb = df.groupby("quarter", as_index=False).agg(
        {
            "High": "max", "Low": "min", "Open": "first", "Close": "last", "Volume": "sum"
        }
    )
    gb['trimester_delta'] = ((gb['Close'] - gb['Open'])/gb['Open'])*100
    gb['traded_volume'] = gb['traded_volume'].shift()
    gb = gb.rename(
        columns={
            "High": "trimester_high",
            "Low": "trimester_low",
            "Volume": "traded_volume",
            "Open": "stock_value"
        }
    )

    return gb


path = "C:/Users/Tulio/PycharmProjects/RL_Doutorado_Lud/SNY.xlsx"
# data = get_data(path)

df = pd.read_excel(path)
df['Date'] = pd.to_datetime(df['Date'])
df['last_day_closing'] = df['Close'].shift()
df['last_day_high'] = df['High'].shift()
df['last_day_low'] = df['Low'].shift()
df['traded_volume'] = df['Volume'].shift()
df['last_day_delta'] = df['High'].shift() - df['Open'].shift()
df['stock_value'] = df['Open']

df = df.iloc[1:]