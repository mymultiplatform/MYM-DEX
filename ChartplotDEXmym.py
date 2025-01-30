import requests
import tkinter as tk
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import random

def fetch_dex_candles():
    """
    Fetch live candlestick data for the jellyjelly/SOL pair.
    """
    base_url = "https://api.dexscreener.com/latest/dex/pairs/solana/3bC2e2RxcfvF9oP22LvbaNsVwoS2T98q6ErCRoayQYdq"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        if "pairs" in data and len(data["pairs"]) > 0:
            pair_data = data["pairs"][0]
            price = float(pair_data.get("priceUsd", 0))
            return price
    except requests.exceptions.RequestException:
        return None
    return None

class CandlestickChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Candlestick Chart")
        self.root.geometry("500x500")
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.data = []  # Stores (timestamp, open, high, low, close)
        self.update_chart()
    
    def update_chart(self):
        def fetch_and_update():
            price = fetch_dex_candles()
            if price is not None:
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                
                if len(self.data) == 0:
                    self.data.append([timestamp, price, price, price, price])
                else:
                    last_candle = self.data[-1]
                    open_price, high, low, close = last_candle[1:]
                    
                    # Simulating candlestick movement
                    new_high = max(high, price + random.uniform(-0.1, 0.1))
                    new_low = min(low, price - random.uniform(-0.1, 0.1))
                    new_close = price
                    
                    if len(self.data) >= 10:
                        self.data.pop(0)
                    self.data.append([timestamp, open_price, new_high, new_low, new_close])
                
                self.redraw_chart()
            self.root.after(3000, self.update_chart)
        
        threading.Thread(target=fetch_and_update, daemon=True).start()
    
    def redraw_chart(self):
        self.ax.clear()
        timestamps = [d[0] for d in self.data]
        opens = [d[1] for d in self.data]
        highs = [d[2] for d in self.data]
        lows = [d[3] for d in self.data]
        closes = [d[4] for d in self.data]
        
        for i in range(len(self.data)):
            color = 'green' if closes[i] >= opens[i] else 'red'
            self.ax.plot([i, i], [lows[i], highs[i]], color='black')
            self.ax.plot([i, i], [opens[i], closes[i]], color=color, linewidth=6)
        
        self.ax.set_xticks(range(len(timestamps)))
        self.ax.set_xticklabels(timestamps, rotation=45)
        self.ax.set_title("JellyJelly / SOL Live Candlestick Chart")
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CandlestickChartApp(root)
    root.mainloop()
