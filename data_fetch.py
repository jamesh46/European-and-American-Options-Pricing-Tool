import yfinance as yf

def fetch_stock_price(ticker):
    """
    Fetches the current stock price for the given ticker symbol.
    
    Returns:
    - Current closing price of the stock.
    """
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period='1d')
    
    # Ensure that stock data is not empty
    if stock_data.empty:
        raise ValueError(f"Could not retrieve stock data for ticker {ticker}.")
    
    return stock_data['Close'].iloc[-1]  # Latest closing price

def fetch_option_chain(ticker, expiry):
    """
    Fetches the option chain for the given ticker symbol and expiration date.
    
    Returns:
    - A tuple containing two DataFrames: (calls, puts).
    """
    stock = yf.Ticker(ticker)
    
    available_expirations = stock.options
    if expiry not in available_expirations:
        raise ValueError(f"Expiration date {expiry} not found for ticker {ticker}. Available dates: {available_expirations}")
    
    options_chain = stock.option_chain(expiry)
    return options_chain.calls, options_chain.puts

def fetch_option_details(ticker, expiry, strike_price, option_type='call'):
    """
    Fetches option details (including bid/ask prices and implied volatility) for the given option.
    
    Returns:
    - A dictionary containing the option's details.
    """
    calls, puts = fetch_option_chain(ticker, expiry)

    if option_type == 'call':
        matching_option = calls[calls['strike'] == strike_price]
    elif option_type == 'put':
        matching_option = puts[puts['strike'] == strike_price]
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    if not matching_option.empty:
        # Check for any missing data points and handle them gracefully
        option_details = {
            'implied_volatility': matching_option['impliedVolatility'].fillna(0).values[0],
            'bid': matching_option['bid'].fillna(0).values[0],
            'ask': matching_option['ask'].fillna(0).values[0],
            'last_price': matching_option['lastPrice'].fillna(0).values[0],
            'strike': strike_price,
            'expiry': expiry,
            'type': option_type
        }
        return option_details
    else:
        raise ValueError(f"Option with strike price {strike_price} not found for {ticker} {option_type} options.")

