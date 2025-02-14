from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Initialize the CoinGecko API
cg = CoinGeckoAPI()

# Function to fetch 20 days of historical price data for DOGE/USD
def fetch_doge_usd_history():
    data = cg.get_coin_market_chart_by_id(id='dogecoin', vs_currency='usd', days=20)
    timestamps = [datetime.datetime.utcfromtimestamp(entry[0] / 1000) for entry in data['prices']]
    prices = [entry[1] for entry in data['prices']]
    return timestamps, prices

# Function to find peaks and troughs in the price data
def find_peaks_and_troughs(prices, timestamps):
    peaks = []
    peak_times = []
    troughs = []
    trough_times = []
    
    for i in range(1, len(prices) - 1):
        if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
            peaks.append(prices[i])
            peak_times.append(timestamps[i])
        elif prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
            troughs.append(prices[i])
            trough_times.append(timestamps[i])
    
    return peaks, peak_times, troughs, trough_times

# Function to detect Break of Structure (BoS)
def detect_bos(prices, peaks, troughs):
    bos = False
    bos_level = None
    bos_index = None
    
    # Check for Break of Structure (uptrend: higher highs and higher lows)
    for i in range(1, len(peaks)):
        if peaks[i] > peaks[i - 1] and troughs[i] > troughs[i - 1]:
            bos = True
            bos_level = peaks[i]
            bos_index = i
    
    return bos, bos_level, bos_index

# Function to calculate Fibonacci retracement levels
def calculate_fibonacci_levels(high, low):
    return {
        '0.236': high - (high - low) * 0.236,
        '0.382': high - (high - low) * 0.382,
        '0.5': high - (high - low) * 0.5,
        '0.618': high - (high - low) * 0.618,
        '0.786': high - (high - low) * 0.786,
    }

# Function to generate the historical price chart with BoS, entry setup, and levels
def generate_historical_chart():
    timestamps, prices = fetch_doge_usd_history()
    
    # Find peaks and troughs
    peaks, peak_times, troughs, trough_times = find_peaks_and_troughs(prices, timestamps)
    
    # Detect Break of Structure (BoS)
    bos, bos_level, bos_index = detect_bos(prices, peaks, troughs)
    
    # Calculate Fibonacci retracement levels
    if bos:
        high = bos_level
        low = troughs[bos_index - 1] if bos_index > 0 else min(prices)
        fib_levels = calculate_fibonacci_levels(high, low)
        
        # Define entry zone (0.618 or 0.5 retracement)
        entry_zone = fib_levels['0.618']
        stop_loss = low  # Stop-loss below the retracement zone
        take_profit = high + (high - low)  # Take-profit at the next resistance level
        
    plt.figure(figsize=(12, 6))  # Set figure size
    plt.plot(timestamps, prices, label='DOGE/USD Price', color='blue')
    
    # Plot peaks and troughs
    plt.scatter(peak_times, peaks, color='red', s=50, label='Peaks')
    plt.scatter(trough_times, troughs, color='green', s=50, label='Troughs')
    
    # Plot Break of Structure (BoS) level
    if bos:
        plt.axhline(y=bos_level, color='orange', linestyle='--', label=f'Break of Structure (BoS) Level (${bos_level:.4f})')
        
        # Plot Fibonacci retracement levels
        for level, value in fib_levels.items():
            plt.axhline(y=value, color='purple', linestyle=':', label=f'Fib {level} (${value:.4f})')
        
        # Plot entry zone, stop-loss, and take-profit
        plt.axhline(y=entry_zone, color='cyan', linestyle='--', label=f'Entry Zone (${entry_zone:.4f})')
        plt.axhline(y=stop_loss, color='black', linestyle='--', label=f'Stop-Loss (${stop_loss:.4f})')
        plt.axhline(y=take_profit, color='magenta', linestyle='--', label=f'Take-Profit (${take_profit:.4f})')
    
    plt.title('DOGE/USD Price Chart (Last 20 Days) with BoS and Entry Setup')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    
    plt.show()

# Run the historical chart
generate_historical_chart()
