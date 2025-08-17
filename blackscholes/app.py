import tkinter as tk
import yfinance as yf
from datetime import datetime
import pandas as pd
from calc import black_scholes, delta_calc, gamma_calc, vega_calc, theta_calc, rho_calc, d1_calc, d2_calc, implied_volatility
from plot import plot_iv_surface
from mpl_toolkits.mplot3d import Axes3D

pd.set_option('display.max_rows', None)

root = tk.Tk()
root.title("Black-Scholes Calculator")
root.geometry("600x600")

# --- Global variables ---
ticker = None
date = tk.StringVar()
option_type = tk.StringVar(value="call")



def load_dates(symbol):
    global ticker, dropdown

    try:
        ticker = yf.Ticker(symbol)
        _ = ticker.fast_info['lastPrice']  # Check if valid ticker
    except:
        print("Invalid ticker")
        return

    # Get available dates
    dates = ticker.options
    date.set(dates[0])  # Set default
    if dropdown:
        dropdown.destroy()  # Remove old dropdown
    dropdown = tk.OptionMenu(root, date, *dates)
    dropdown.pack()


def start_calc(option_type, ticker, date):
    if not ticker:
        print("Ticker not loaded")
        return
    
    T = (pd.to_datetime(date.get()) - pd.to_datetime(datetime.now())).days / 365
    option_chain = pd.DataFrame(getattr(ticker.option_chain(date.get()), option_type.get()))
    
    columns_to_drop = ['lastTradeDate', 'volume', 'openInterest', 'contractSize', 'currency', 'inTheMoney', 'bid', 'ask', 'change', 'percentChange']
    option_chain.drop(columns=[col for col in columns_to_drop if col in option_chain.columns], inplace=True)

    option_chain["BS Price"] = option_chain.apply(
        lambda row: black_scholes(S=ticker.fast_info['lastPrice'], K=row["strike"], T=T, r=0.01, sigma=row["impliedVolatility"], option_type=option_type.get()),
        axis=1)

    option_chain['delta'] = option_chain.apply(lambda row: delta_calc(S=row['lastPrice'], K=row['strike'], sigma=row['impliedVolatility'], T=T, r=0.01), axis=1)
    option_chain['gamma'] = option_chain.apply(lambda row: gamma_calc(S=row['lastPrice'], K=row['strike'], sigma=row['impliedVolatility'], T=T, r=0.01), axis=1)
    option_chain['vega'] = option_chain.apply(lambda row: vega_calc(S=row['lastPrice'], K=row['strike'], sigma=row['impliedVolatility'], T=T, r=0.01), axis=1)
    option_chain['theta'] = option_chain.apply(lambda row: theta_calc(S=row['lastPrice'], K=row['strike'], sigma=row['impliedVolatility'], T=T, r=0.01), axis=1)
    option_chain['rho'] = option_chain.apply(lambda row: rho_calc(S=row['lastPrice'], K=row['strike'], sigma=row['impliedVolatility'], T=T, r=0.01), axis=1)

    option_chain_cleaned = option_chain[(option_chain["impliedVolatility"] >= 0.05) &
    (option_chain["vega"] > 1e-5)].copy()
    option_chain_cleaned.reset_index(drop=True)
    
    print(option_chain_cleaned.head(100))

def create_iv_surface(symbol, option_type):
    print("starting iv surface creation...")
    try:
        ticker = yf.Ticker(symbol)
        _ = ticker.fast_info["lastPrice"]  # Check if valid ticker
    except:
        print("Invalid ticker")
        return
    moneyness =[]
    dtes = []
    ivs = []

    
    for expiry in ticker.options:
        T   = (pd.to_datetime(expiry) - pd.to_datetime(datetime.now())).days / 365
        opt_chain = ticker.option_chain(expiry)
        

        if option_type == "calls":
            data = opt_chain.calls
        else:
            data = opt_chain.puts

        
        for _, row in data.iterrows():
            moneyness.append(ticker.fast_info['lastPrice'] / row['strike'])
            dtes.append(T)
            ivs.append(implied_volatility(S=ticker.fast_info['lastPrice'], K=row['strike'], T=T, r=0.01, market_price=row['lastPrice'], option_type=option_type))
       
        ivs_cleaned = [ivs[i] for i, m in enumerate(moneyness) if m < 2.4 and m > 0.5 and not ivs[i] is None]
        dtes_cleaned = [dtes[i] for i, m in enumerate(moneyness) if m < 2.4 and m > 0.5]
        moneyness_cleaned = [m for m in moneyness if m < 2.4 and m > 0.5]


    plot_iv_surface(moneyness_cleaned, dtes_cleaned, ivs_cleaned)


label = tk.Label(root, text="Enter stock ticker:")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack()

load_button = tk.Button(root, text="Submit ticker and Load Options", command=lambda: load_dates(entry.get()))
load_button.pack(pady=5)

dropdown = None  
option_type_frame = tk.Frame(root)
tk.Radiobutton(option_type_frame, text="Call", variable=option_type, value="calls").pack(side=tk.LEFT)
tk.Radiobutton(option_type_frame, text="Put", variable=option_type, value="puts").pack(side=tk.LEFT)
option_type_frame.pack()

submit_button = tk.Button(root, text="Calculate BS price & greeks", command=lambda: start_calc(option_type, ticker, date))
submit_button.pack(pady=5)

tk.Button(root, text="Create Implied volatility surface", command = lambda: create_iv_surface(entry.get(), option_type.get())).pack(pady=5)

root.mainloop()