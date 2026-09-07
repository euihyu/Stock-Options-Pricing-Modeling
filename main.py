import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

import binomial_model
import black_scholes_model
import monte_carlo_simulation

"""
Takes a stock ticker, fetches live market data, and prices an option on it.
Computes Black-Scholes / binomial tree / Monte Carlo simultaneously and shows a comparison table.
The risk-free rate is also fetched live (13-week US T-bill, ^IRX) instead of using a fixed value.
"""
def ticker_exists(symbol: str) -> bool:
    try:
        recent = yf.Ticker(symbol).history(period="5d")
        return not recent.empty
    except Exception:
        return False

def fetch_price_and_volatility(symbol: str):
    """
    Compute the current price (spot) and annualized volatility (annual_vol)
    """
    end = datetime.now()
    start = end - timedelta(days=365)
    closes = yf.Ticker(symbol).history(start=start, end=end)["Close"]

    spot = closes.iloc[-1]
    annual_vol = closes.pct_change().std() * np.sqrt(252)
    return spot, annual_vol


def fetch_risk_free_rate(fallback: float = 0.0436) -> float:
    """Fetch the US 13-week T-bill rate (^IRX) live and use it as the
    risk-free rate."""
    try:
        quote = yf.Ticker("^IRX").history(period="5d")["Close"].iloc[-1]
        return float(quote) / 100
    except Exception:
        print(f"Could not fetch the risk-free rate, using default  {fallback * 100:.2f}%.")
        return fallback


def price_all_models(spot, strike, expiry, rate, vol, steps, option_type):
    return {
        "Black-Scholes": black_scholes_model.black_scholes_model(
            spot, strike, expiry, rate, vol, option_type=option_type
        ),
        "Binomial": binomial_model.binomial_price(
            spot, strike, expiry, rate, vol, n=steps, option_type=option_type
        ),
        "Monte Carlo": monte_carlo_simulation.monte_carlo_simulation(
            spot, strike, expiry, rate, vol, n=steps, option_type=option_type
        ),
    }


def run():
    symbol = input("Enter the stock ticker to price an option on: ").upper()
    while not ticker_exists(symbol):
        symbol = input("Invalid ticker. Try again: ").upper()

    spot, annual_vol = fetch_price_and_volatility(symbol)
    rate = fetch_risk_free_rate()

    strike = spot  #  assume an at-the-money option
    expiry = 30 / 252
    steps = 1000  #  binomial tree steps / Monte Carlo simulation count

    print(
        f"\n{symbol}  Spot: {spot:.2f}   "
        f"Annualized volatility: {annual_vol * 100:.2f}%   "
        f"Risk-free rate: {rate * 100:.2f}%\n"
    )

    call_prices = price_all_models(spot, strike, expiry, rate, annual_vol, steps, "call")
    put_prices = price_all_models(spot, strike, expiry, rate, annual_vol, steps, "put")

    print(f"{'Model':<18}{'Call':>12}{'Put':>12}")
    print("-" * 42)
    for model_name in ("Black-Scholes", "Binomial", "Monte Carlo"):
        print(f"{model_name:<18}{call_prices[model_name]:>12.4f}{put_prices[model_name]:>12.4f}")


if __name__ == "__main__":
    run()