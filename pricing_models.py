import numpy as np
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Black-Scholes Model for European Options
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """
    Prices a European option using the Black-Scholes formula.
    """
    # Check if input parameters are valid
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        raise ValueError("Invalid input values for option pricing.")

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Option type must be 'call' or 'put'")

# Binomial Tree Model for American Options
def binomial_tree_american_option(S, K, T, r, sigma, option_type='call', num_steps=100):
    """
    Prices an American option using the Binomial Tree method.
    """
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0 or num_steps <= 0:
        raise ValueError("Invalid input values for option pricing.")

    dt = T / num_steps  # Time per step
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Probability of up move
    discount_factor = np.exp(-r * dt)  # Discount factor per step

    asset_prices = np.zeros((num_steps + 1, num_steps + 1))
    asset_prices[0, 0] = S

    for i in range(1, num_steps + 1):
        asset_prices[i, 0] = asset_prices[i - 1, 0] * u
        for j in range(1, i + 1):
            asset_prices[i, j] = asset_prices[i - 1, j - 1] * d

    option_values = np.zeros((num_steps + 1, num_steps + 1))

    for j in range(num_steps + 1):
        if option_type == 'call':
            option_values[num_steps, j] = max(0, asset_prices[num_steps, j] - K)
        elif option_type == 'put':
            option_values[num_steps, j] = max(0, K - asset_prices[num_steps, j])

    for i in range(num_steps - 1, -1, -1):
        for j in range(i + 1):
            continuation_value = (p * option_values[i + 1, j] + (1 - p) * option_values[i + 1, j + 1]) * discount_factor
            exercise_value = max(asset_prices[i, j] - K, 0) if option_type == 'call' else max(K - asset_prices[i, j], 0)
            option_values[i, j] = max(continuation_value, exercise_value)

    return option_values[0, 0]

# Monte Carlo Longstaff-Schwartz for American Options
def monte_carlo_longstaff_schwartz(S, K, T, r, sigma, option_type='call', num_simulations=50000, num_steps=100):
    """
    Prices an American option using the Monte Carlo Longstaff-Schwartz method
    and visualizes the simulated stock price paths, along with an average path.
    
    Parameters:
    - S: Current stock price
    - K: Option strike price
    - T: Time to expiration in years
    - r: Risk-free interest rate
    - sigma: Volatility of the underlying stock
    - option_type: 'call' or 'put'
    - num_simulations: Number of Monte Carlo simulations (default is 50,000)
    - num_steps: Number of steps in the simulation

    Returns:
    - Price of the American option
    """
    dt = T / num_steps  # Time step
    discount_factor = np.exp(-r * dt)

    # Simulate stock price paths
    stock_paths = np.zeros((num_simulations, num_steps + 1))
    stock_paths[:, 0] = S

    for t in range(1, num_steps + 1):
        Z = np.random.standard_normal(num_simulations)
        stock_paths[:, t] = stock_paths[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    # Calculate the average stock price path
    average_path = np.mean(stock_paths, axis=0)
    
    # Plot the paths
    plt.figure(figsize=(10, 6))
    
    # Plot all paths in dark grey with low alpha for transparency
    for i in range(num_simulations):  
        plt.plot(np.linspace(0, T, num_steps + 1), stock_paths[i], color='darkgrey', lw=0.5, alpha=0.1)

    # Plot the average path in red and bold
    plt.plot(np.linspace(0, T, num_steps + 1), average_path, color='red', lw=2, label='Average Path')

    # Adjust the y-axis limits to zoom in on the stock price evolution
    plt.ylim([0.8 * S, 1.2 * S])  # Zoom in around the initial stock price

    plt.title("Simulated Stock Price Paths with Average Path")
    plt.xlabel("Time (Years)")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Initialize payoff matrix
    payoffs = np.zeros_like(stock_paths)

    # Calculate payoff at each step
    for t in range(num_steps + 1):
        if option_type == 'call':
            payoffs[:, t] = np.maximum(stock_paths[:, t] - K, 0)
        else:
            payoffs[:, t] = np.maximum(K - stock_paths[:, t], 0)

    # Start backward induction
    option_values = payoffs[:, -1]  # Payoff at maturity
    for t in range(num_steps - 1, 0, -1):
        continuation_value = option_values * discount_factor
        
        in_the_money = payoffs[:, t] > 0
        X = stock_paths[in_the_money, t].reshape(-1, 1)
        Y = continuation_value[in_the_money]

        reg = LinearRegression().fit(X, Y)
        estimated_continuation_value = reg.predict(X)

        exercise = payoffs[in_the_money, t] > estimated_continuation_value
        option_values[in_the_money] = np.where(exercise, payoffs[in_the_money, t], continuation_value[in_the_money])

    return np.mean(option_values) * discount_factor
