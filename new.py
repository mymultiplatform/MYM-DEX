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

# Function to find peaks in the price data
def find_peaks(prices, timestamps):
    peaks = []
    peak_times = []
    for i in range(1, len(prices) - 1):
        if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
            peaks.append(prices[i])
            peak_times.append(timestamps[i])
    return peaks, peak_times

# Function to generate the historical price chart with resistance line
def generate_historical_chart():
    timestamps, prices = fetch_doge_usd_history()
    
    # Find peaks
    peaks, peak_times = find_peaks(prices, timestamps)
    
    # Calculate the average of the peaks to determine the resistance level
    resistance_level = np.mean(peaks)
    
    plt.figure(figsize=(10, 5))  # Set figure size
    plt.plot(timestamps, prices, label='DOGE/USD Price', color='blue')
    
    # Plot the resistance level as a horizontal red line
    plt.axhline(y=resistance_level, color='red', linestyle='--', label=f'Resistance Level (${resistance_level:.4f})')
    
    # Plot small red circles on top of the peaks
    plt.scatter(peak_times, peaks, color='red', s=50, label='Peaks')
    
    plt.title('DOGE/USD Price Chart (Last 20 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    
    plt.show()

# Run the historical chart
generate_historical_chart()
