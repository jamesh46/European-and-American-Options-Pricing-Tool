import tkinter as tk
from tkinter import messagebox
from data_fetch import fetch_stock_price, fetch_option_details
from pricing_models import black_scholes_price, binomial_tree_american_option, monte_carlo_longstaff_schwartz
import numpy as np
import matplotlib.pyplot as plt
import threading

def calculate_option_price():
    # Clear the previous output
    result_label.config(text="")
    recommendation_label.config(text="")
    alternative_label.config(text="")
    calculating_label.config(text="Calculating...")  # Show "Calculating..."

    # Run the calculations in a separate thread to avoid freezing the UI
    threading.Thread(target=perform_calculation).start()

def perform_calculation():
    try:
        ticker = ticker_entry.get().upper()
        expiry = expiry_entry.get()
        strike_price = float(strike_entry.get())
        option_type = option_type_var.get().lower()
        option_style = option_style_var.get().lower()
        pricing_method = pricing_method_var.get()  # Get the selected pricing method

        if not ticker or not expiry or strike_price <= 0:
            raise ValueError("Please provide valid inputs for all fields.")

        stock_price = fetch_stock_price(ticker)
        option_details = fetch_option_details(ticker, expiry, strike_price, option_type)

        if option_details:
            implied_volatility = option_details['implied_volatility']
            bid_price = option_details['bid']
            ask_price = option_details['ask']
            last_price = option_details['last_price']
            time_to_expiry = (np.datetime64(expiry) - np.datetime64('today')) / np.timedelta64(365, 'D')
            risk_free_rate = 0.01

            # Continue with pricing calculations
            if pricing_method == 'Black-Scholes':
                if option_style == 'european':
                    fair_value = black_scholes_price(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility, option_type)
                else:
                    messagebox.showerror("Error", "Black-Scholes can only price European options.")
                    calculating_label.config(text="")  # Remove "Calculating..."
                    return
            elif pricing_method == 'Binomial Tree':
                fair_value = binomial_tree_american_option(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility, option_type)
            elif pricing_method == 'Monte Carlo (Longstaff-Schwartz)':
                fair_value = monte_carlo_longstaff_schwartz(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility, option_type)
            
            # Update the UI with the fair value and market prices
            result_label.config(text=f"Fair Value: ${fair_value:.2f}\nBid Price: ${bid_price:.2f}, Ask Price: ${ask_price:.2f}\nLast Price: ${last_price:.2f}")

            # Check for illiquid options with 0.00 bid/ask prices
            if bid_price == 0.00 and ask_price == 0.00:
                recommendation_label.config(text="This option has low liquidity (bid/ask are 0.00).")
            else:
                # Determine whether to buy, sell, or hold
                recommendation = make_recommendation(fair_value, bid_price, ask_price)
                recommendation_label.config(text=f"Recommendation: {recommendation}")

            # Provide alternative suggestions if needed
            suggestion = suggest_alternative(ticker, expiry, option_type)
            alternative_label.config(text=f"Suggested Alternative: {suggestion}")

        else:
            messagebox.showerror("Error", "Option data not found.")

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        calculating_label.config(text="")  # Remove "Calculating..." once done


def make_recommendation(fair_value, bid, ask):
    if fair_value > ask * 1.05:
        return 'Strong Buy'
    elif fair_value > ask:
        return 'Buy'
    elif fair_value < bid * 0.95:
        return 'Strong Sell'
    elif fair_value < bid:
        return 'Sell'
    else:
        return 'Hold'

def suggest_alternative(ticker, expiry, option_type):
    return f"Consider different strikes with {expiry} expiration for {ticker} {option_type} options."

# GUI Setup
root = tk.Tk()
root.title("Option Pricing Application")

tk.Label(root, text="Stock Ticker:").grid(row=0, column=0)
ticker_entry = tk.Entry(root)
ticker_entry.grid(row=0, column=1)

tk.Label(root, text="Expiration Date (YYYY-MM-DD):").grid(row=1, column=0)
expiry_entry = tk.Entry(root)
expiry_entry.grid(row=1, column=1)

tk.Label(root, text="Strike Price:").grid(row=2, column=0)
strike_entry = tk.Entry(root)
strike_entry.grid(row=2, column=1)

option_type_var = tk.StringVar(value="call")
tk.Label(root, text="Option Type:").grid(row=3, column=0)
tk.Radiobutton(root, text="Call", variable=option_type_var, value="call").grid(row=3, column=1)
tk.Radiobutton(root, text="Put", variable=option_type_var, value="put").grid(row=3, column=2)

option_style_var = tk.StringVar(value="european")
tk.Label(root, text="Option Style:").grid(row=4, column=0)
tk.Radiobutton(root, text="European", variable=option_style_var, value="european").grid(row=4, column=1)
tk.Radiobutton(root, text="American", variable=option_style_var, value="american").grid(row=4, column=2)

pricing_method_var = tk.StringVar(value="Black-Scholes")
tk.Label(root, text="Pricing Method:").grid(row=5, column=0)
pricing_method_menu = tk.OptionMenu(root, pricing_method_var, "Black-Scholes", "Binomial Tree", "Monte Carlo (Longstaff-Schwartz)")
pricing_method_menu.grid(row=5, column=1)

calculate_button = tk.Button(root, text="Calculate Option Price", command=calculate_option_price)
calculate_button.grid(row=6, column=0, columnspan=3)

# Label to show calculating text
calculating_label = tk.Label(root, text="")
calculating_label.grid(row=7, column=0, columnspan=3)

# Labels to display the result and recommendations
result_label = tk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=3)

recommendation_label = tk.Label(root, text="")
recommendation_label.grid(row=9, column=0, columnspan=3)

alternative_label = tk.Label(root, text="")
alternative_label.grid(row=10, column=0, columnspan=3)

root.mainloop()


