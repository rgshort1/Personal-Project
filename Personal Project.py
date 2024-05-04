#%% compare sectors of the stock market
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def calculate_returns(data):
    returns = data.pct_change().dropna()
    return returns

def show_chart(data):
    cumulative_returns = (1 + data.pct_change()).cumprod()
    cumulative_returns.plot(figsize=(10, 5))
    plt.title('Cumulative Returns')
    plt.show()

def show_volatility(data):
    volatility = data.pct_change().std() * (252**0.5)  # Annualized Volatility
    plt.figure(figsize=(10, 5))
    volatility.plot(kind='bar')
    plt.title('Annualized Volatility')
    plt.show()

def show_correlation(data):
    correlation = data.pct_change().corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

def submit():
    selections = [sectors[sector] for sector in sectors if var_dict[sector].get()]
    if not selections:
        messagebox.showerror('Error', 'Please select at least one sector')
        return
    
    data = fetch_data(selections + ['SPY'], '2020-01-01', '2023-01-01')
    show_chart(data)
    show_volatility(data)
    show_correlation(data.pct_change().dropna())

# UI setup
root = tk.Tk()
root.title("Sector Analysis Tool")

sectors = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Financials': 'XLF',
    'Industrials': 'XLI'
}

var_dict = {sector: tk.BooleanVar() for sector in sectors}

for sector, var in var_dict.items():
    tk.Checkbutton(root, text=sector, variable=var).pack(anchor='w')

ttk.Button(root, text="Submit", command=submit).pack()

root.mainloop()






# %%
