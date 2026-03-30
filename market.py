import yfinance as yf

def get_market_data():
    uber = yf.Ticker("UBER")
    lyft = yf.Ticker("LYFT")

    df = uber.history(period="5d", interval="1h")

    latest_price = df["Close"].iloc[-1]
    prev_price = df["Close"].iloc[-10]

    momentum = (latest_price - prev_price) / prev_price

    volume_now = df["Volume"].iloc[-1]
    volume_avg = df["Volume"].mean()

    volume_spike = volume_now / volume_avg

    return {
        "price": round(latest_price, 2),
        "momentum": momentum,
        "volume_spike": volume_spike
    }