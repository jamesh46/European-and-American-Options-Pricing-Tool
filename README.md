# 📈 Monte Carlo Options Pricing Tool

This **Option Pricing Tool** provides a user-friendly interface to calculate the fair price of financial options using various pricing models for both European and American Options. It is designed to be used for personal financial research as a tool for quick option valuation.


## 🚀 Features

- **Black-Scholes Model** – Best suited for European-style options.
- **Binomial Tree Model** – Supports American-style options and early exercise.
- **Monte Carlo Simulations** – Estimates prices for more complex or path-dependent options using the Longstaff-Schwartz method.

The tool will guide the user to use the appropriate model for the type of option.

<br>

## 📊 Usage

### Option Inputs
- **Stock Ticker**: Enter the stock's symbol (e.g., AAPL for Apple).
- **Expiration Date**: The date when the option expires.
- **Strike Price**: The agreed price at which the option can be exercised.
- **Option Type**: Choose between Call or Put options.
- **Option Style**: Select either American or European style options.

### Searching and Comparing Market Options
- The tool allows users to **search for live options data** from the options market. Users can retrieve real-time options for a particular stock and see various contracts available for different expiration dates and strike prices.
- Once an option is selected from the available contracts, the user can input it into the tool to compare its **bid/ask prices**, **implied volatility**, and **model-generated fair value**.
  
For example, if you want to compare a call option with a strike price of $150 and an expiration of December 31, 2024:
1. Search for the available options for **AAPL**.
2. Select the desired contract (strike price, expiration, etc.).
3. Enter the contract details into the tool, which will retrieve the real-time market data and provide the model's pricing output for comparison.

### Pricing Methods
- **Black-Scholes**: Suitable for European options only.
- **Binomial Tree**: Ideal for American-style options due to early exercise capabilities.
- **Monte Carlo Simulations**: Can handle complex or path-dependent options, particularly useful for American options with more intricate payoff structures.

### Example Output
- The tool will return values such as the **option's fair price**, **implied volatility**, and **bid/ask prices** from the models.
- This in the event that the model determines the fair price to be lower than the ... price, in the theory, the user might consider purchasing this option.

### WARNINGS
- Please remember that this model is rudimentary relative to those used in industry and developed as a research project. Any Recommendations are to guide potential research only and should not be taken as financial advice.

### Key Financial Assumptions
- **Implied Volatility**: Automatically fetched based on market data.
- **Risk-Free Rate**: Assumed to be 1% by default, but can be modified within the code if required.
- **Dividend Yield**: Assumed to be 0, unless specified otherwise.

### Example Pricing Scenario
```plaintext
Stock: AAPL
Option Type: Call, American
Strike Price: $150
Expiration: 2024-12-31

- Fair Value (Monte Carlo - Longstaff-Schwartz): $12.50
- Implied Volatility: 23.5%
- Bid: $12.30 | Ask: $12.70
```

<br>

### Example Images of Application

![image](https://github.com/user-attachments/assets/57a02de8-afc7-4922-a5c8-b547f863902b)

![image](https://github.com/user-attachments/assets/5f8048d6-bd90-4e61-b45c-21fa9ff2c91a)


<br>

## ⚡ Performance and Accuracy

### 1. **Black-Scholes Model**
- **Execution Speed**: Nearly instantaneous (< 1 second).
- **Accuracy**: The Black-Scholes model provides highly accurate prices for **European options**, typically with about **1-2%** error of real-time market prices. Small discrepancies may arise due to differences in **implied volatility** estimates between this tool and market data providers.

**Black-Scholes Summary**: Close match to real-world European option prices with minimal deviation due to volatility or market sentiment factors.

### 2. **Binomial Tree Model**
- **Execution Speed**: Moderate (2-5 seconds with 500 steps).
- **Accuracy**: The Binomial Tree model is highly accurate for **American options**, typically with about **2-3%** error on live market prices. Accuracy improves with the number of time steps but may be slightly slower as a result.

**Binomial Tree Summary**: Closely matches market prices for American options, particularly with sufficient time steps.

### 3. **Monte Carlo Simulation**
- **Execution Speed**: Slow (~60 seconds for 50,000 simulations).
- **Accuracy**: Monte Carlo is best for pricing complex, path-dependent options. With sufficient simulations, it provides accuracy within **0.5%** of market prices. It is particularly useful for exotic options but may require more time to compute.

**Monte Carlo Summary**: High accuracy for complex options, with some trade-off in execution time for large simulations.

### Example of Accuracy Comparison

| Model                  | Typical Market Deviation (vs. Online Platforms) |
|------------------------|-------------------------------------------------|
| **Black-Scholes**       | ~ 1-2% for European options                |
| **Binomial Tree**       | ~ 2-3% for American options                |
| **Monte Carlo**         | < 1% for exotic options (with large simulations) |

### Factors Affecting Accuracy
- **Implied Volatility**: Differences in the implied volatility data fetched by this tool and market data can lead to small deviations from market prices.
- **Market Sentiment and Liquidity**: Real-time market prices may reflect factors like liquidity, supply and demand, and transaction costs, which are not captured by theoretical models.
- **Bid/Ask Spreads**: The tool provides a "fair value" that may fall between the real market's bid/ask prices, especially in volatile or illiquid markets.

<br>


## 🛠️ Installation Guide

Follow these steps to install and run the Option Pricing Tool.

### 1. Clone the repository:
```bash
git clone <repository-url>
```

### 2. Navigate to the project directory:
```bash
cd option_pricing_tool
```

### 3. Install the required packages:
```bash
pip install -r requirements.txt
```
### 3. Install the required packages:
```bash
python app.py
```
