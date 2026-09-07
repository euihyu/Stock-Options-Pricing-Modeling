# Option Pricing Engine

A Python tool that takes a single stock ticker, pulls live market data, and
prices an option on it using three different methods — then compares the
results side by side.

```
$ python main.py
Enter the stock ticker to price an option on: AAPL

AAPL  Spot: 227.52   Annualized volatility: 28.41%   Risk-free rate: 4.32%

Model                     Call         Put
------------------------------------------
Black-Scholes           5.9821      4.5033
Binomial                5.9803      4.5017
Monte Carlo             5.8477      4.6210
```

## Features

- Just enter a ticker — spot price, volatility, and the risk-free rate are all fetched live
- Prices the option with three models at once: Black-Scholes, Binomial, and Monte Carlo
- Prints both call and put prices side by side
- Automatically re-prompts if you enter an invalid ticker

## Usage
Run the script:
bash
  $ python main.py
When prompted, type a stock ticker (e.g. AAPL, TSLA) and press Enter.
If the ticker doesn't exist, you'll be asked to enter one again.
The tool prints the spot price, annualized volatility, risk-free rate, and a comparison table of call/put prices from all three models — see the example at the top of this README.

Enter a ticker (e.g. `AAPL`, `TSLA`) when prompted, and the results print immediately.

## How it works

1. Checks that the ticker you entered actually exists
2. Computes the current price and annualized volatility from the last year of daily closes
3. Fetches the 13-week US T-bill yield (`^IRX`) as the risk-free rate (falls back to a default if that fails)
4. Prices a 30-day, at-the-money option with all three models using the same inputs
5. Prints call and put prices in a comparison table

## Customization

The defaults live inside the `run()` function in `main.py`.

| What to change | Where |
|---|---|
| Expiry (currently 30 days) | `expiry = 30 / 252` |
| Strike (currently at-the-money) | `strike = spot` |
| Binomial tree steps / Monte Carlo simulation count | `steps = 1000` |
| American-style (early exercise) option | `binomial_model.binomial_price(..., american=True)` |

## Models

- **Black-Scholes** — the classic closed-form formula for pricing European options directly from a single equation.
- **Binomial** — models the stock price moving up or down at each step, then works backward from expiry to today's price. Also supports American-style (early exercise) options.
- **Monte Carlo** — simulates thousands of random stock price paths and discounts the average payoff to estimate the price.

All three models take the same inputs (spot, strike, expiry, rate, volatility), so their outputs are directly comparable.

