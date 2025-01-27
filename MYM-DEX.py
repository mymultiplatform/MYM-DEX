
#🏧MYM-A CATEGORY 




import requests
import time

# List of token contract addresses
tokens = [
    {"symbol": "WETH", "address": "0xC02aaa39b223FE8D0a0e5C4F27eAD9083C756Cc2"},
    {"symbol": "USDT", "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"},
    {"symbol": "PEPE", "address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933"},
    {"symbol": "SHIBA", "address": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"},
    {"symbol": "BTC", "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"},
    {"symbol": "SOL", "address": "0x7D6024b28B0b464bE3b83945Fb80c82dbEc89bb8"},
    {"symbol": "MATIC", "address": "0x7d1Afa7B718fb893dB30A3abc0Cfc608AaCfebb0"},
    {"symbol": "DOGE", "address": "0x4206931337dc273a630d328dA6441786BfaD668f"},
    {"symbol": "UNI", "address": "0xF29e46887FFAE92f1ff87DfE39713875Da541373"},
    {"symbol": "LINK", "address": "0x514910771AF9Ca656af840dff83E8264EcF986CA"}
]

# Function to fetch prices
def fetch_prices(tokens):
    api_url = "https://api.dexscreener.com/latest/dex/tokens/"
    prices = {}

    for token in tokens:
        response = requests.get(api_url + token['address'])
        if response.status_code == 200:
            data = response.json()
            if data.get("pair"):
                prices[token["symbol"]] = float(data["pair"]["priceUsd"])
            else:
                prices[token["symbol"]] = None
        else:
            prices[token["symbol"]] = None
    return prices

# Function to detect pullbacks
def detect_pullbacks(price_history, threshold):
    pullbacks = {}
    for symbol, prices in price_history.items():
        if len(prices) >= 3:  # Ensure at least 3 data points
            # Calculate % change from the latest price to 3rd last
            current_price = prices[-1]
            reference_price = prices[-3]  # Price 3 updates ago
            change = ((current_price - reference_price) / reference_price) * 100

            # Check if the change exceeds the threshold (negative for pullback)
            if change <= -threshold:
                pullbacks[symbol] = {
                    "current_price": current_price,
                    "reference_price": reference_price,
                    "percentage_change": round(change, 2),
                }
    return pullbacks

# Main function to track and detect pullbacks
def track_and_detect_pullbacks(threshold=10, interval=60):
    price_history = {token["symbol"]: [] for token in tokens}

    while True:
        # Fetch current prices
        current_prices = fetch_prices(tokens)
        print("Fetched Prices:", current_prices)

        # Update price history
        for symbol, price in current_prices.items():
            if price is not None:
                price_history[symbol].append(price)
                # Limit the price history to the last 3 entries
                if len(price_history[symbol]) > 3:
                    price_history[symbol].pop(0)

        # Detect pullbacks
        pullbacks = detect_pullbacks(price_history, threshold)
        if pullbacks:
            print("\nDetected Pullbacks:")
            for symbol, details in pullbacks.items():
                print(f"{symbol}: {details}")

        print("\nWaiting for next update...\n")
        time.sleep(interval)  # Wait for the next interval

# Start tracking with a 10% pullback threshold
track_and_detect_pullbacks(threshold=10, interval=60)
