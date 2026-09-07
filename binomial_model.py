"""
Builds a CRR binomial tree to price European/American options. As the
number of steps (N) increases, the result converges to the Black-Scholes
theoretical price.
"""
import numpy as np

def binomial_price(s: float, k: float, t: float, r: float, sigma: float, n=200, option_type="call", american=False):
    """
    True for an American (early-exercise) option, False for European
    """
    dt = t / n
    u = np.exp(sigma * np.sqrt(dt))  # up factor
    d = 1 / u  # down factor (so that u*d =1)
    disc = np.exp(-r * dt)  # discount factor for one step
    p = (np.exp(r * dt) - d) / (u - d)  # risk-neutral probability of an up move

    if not (0 < p < 1):
        raise ValueError("Risk-neutral probability is outside (0,1). Increase n or check the outputs.")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be call' or 'put'")

    # Underlying prices at maturity, computed as one vector (j = number of up moves 0..n)
    j = np.arange(n + 1)
    asset_prices = s * u ** j * d ** (n - j)

    # payoff at maturity
    if option_type == "call":
        values = np.maximum(asset_prices - k, 0.0)
    else:
        values = np.maximum(k - asset_prices, 0.0)

    # backward induction
    for _ in range(n - 1, -1, -1):
        # Underlying prices one step earlier: drop the top node and divide by d
        # (e.g. N=2 -> [S*d^2, S*u*d, S*u^2]; drop the last element and divide
        #  by d to get the N=1 prices [S*d, S*u])
        asset_prices = asset_prices[:-1] / d
        continuation = disc * (p * values[1:] + (1 - p) * values[:-1])

        if american:
            if option_type == "call":
                exercise = np.maximum(asset_prices - k, 0.0)
            else:
                exercise = np.maximum(k - asset_prices, 0.0)
            values = np.maximum(continuation, exercise)
        else:
            values = continuation

    return float(values[0])


