from data_fetch import fetch_stock_price, fetch_option_details
from pricing_models import black_scholes_price, monte_carlo_american_option
import numpy as np

if __name__ == '__main__':
    # Example parameters
    ticker = 'AAPL'
    expiry = '2024-12-20'
    strike_price = 150.00
    option_type = 'call'
    option_style = 'american'  # 'american' or 'european'

    # Fetch stock price
    stock_price = fetch_stock_price(ticker)
    print(f"The current price of {ticker} is ${stock_price:.2f}")

    # Fetch option details
    option_details = fetch_option_details(ticker, expiry, strike_price, option_type)

    if option_details:
        # Extract relevant data
        implied_volatility = option_details['implied_volatility']
        print(f"Implied Volatility: {implied_volatility:.2f}")
        
        # Calculate time to expiration in years
        time_to_expiry = (np.datetime64(expiry) - np.datetime64('today')) / np.timedelta64(365, 'D')
        risk_free_rate = 0.01  # Example risk-free rate

        # Use the appropriate model based on option style
        if option_style == 'european':
            option_price = black_scholes_price(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility, option_type)
        elif option_style == 'american':
            option_price = monte_carlo_american_option(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility, option_type)
        else:
            raise ValueError("Option style must be 'american' or 'european'")

        print(f"The price of the {option_type} option is: ${option_price:.2f}")
    else:
        print(f"No {option_type} option found for strike price {strike_price}.")
