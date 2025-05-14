import yfinance as yf 
import pandas as pd 

def fetch_asset_data()->pd.DataFrame:
    btc = yf.Ticker("BTC-USD").history(period = "max")
    tsla = yf.Ticker("TSLA").history(period="max")
    eth = yf.Ticker("ETH-USD").history(period="max")
    
    for df in [btc,tsla, eth]:
        if isinstance(df.index, pd.DatatimeIndex):
            df.index = df.index.tz_localize(None)
            
    btc["Company"]="BTC"
    tsla["Company"]="TSLA"
    eth["Company"]="ETH"

    df = pd.concat([btc,tsla,eth]).reset_index()
    df = df.dropna().drop_duplicates().reset_index(drop=True)
    df['Date']=pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Company','Date'])

    df['Closing_change_percent_24h'] = df.groupby(['Company'])['Close'].pct_change()*100 
    df['Closing_change_percent_24h'] = df['Closing_change_percent_24h'].fillna(0)
    df['Average_ClosingPrice_7d'] = df.groupby('Company')['Close'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )

    latest_close = df.groupby('Company')['Close'].transform('last')
    df['Latest Price'] = latest_close 

    return df 