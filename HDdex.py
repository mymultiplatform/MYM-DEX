import requests

TOKEN_ADDRESS = "3bC2e2RxcfvF9oP22LvbaNsVwoS2T98q6ErCRoayQYdq"
INTERVAL = "5m"  # Change to 1h, 1d to test longer history

url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{TOKEN_ADDRESS}/candles?interval={INTERVAL}"
response = requests.get(url).json()

if "candles" in response:
    for candle in response["candles"]:
        print(f"Time: {candle['timestamp']}, Open: {candle['open']}, Close: {candle['close']}")
else:
    print("No historical data available.")
