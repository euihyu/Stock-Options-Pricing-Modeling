from scipy.stats import norm
import math

def black_scholes_model(s: float, k: float, t: float, r: float, sigma: float,
                   option_type: str = 'call'):
    """
    :param s: current stock price
    :param k: strike price
    :param t: period to expiration
    :param r: risk-free rate
    :param sigma: volatility of underlying asset
    :param option_type: type of the option w/ call option as default
    :return: fair value of the premium for the options contract
    """
    d1 = (math.log(s / k) + (r + sigma ** 2 / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    if option_type == 'call':
        return s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)
    elif option_type == 'put':
        return k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be either 'call' or 'put'.")