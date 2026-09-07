import numpy as np
import math

def monte_carlo_simulation(s: float, k: float, t: float, r: float, sigma: float, n: int, option_type: str = 'call'):
        """
            s, k, t, r, sigma: same variable as black shcholes model
            n_sims: 시뮬레이션(경로) 횟수
            option_type: "call" or "put"
        """
        Z = np.random.standard_normal(n)
        ST = s * np.exp((r - 0.5 * sigma ** 2) * t + sigma * math.sqrt(t) * Z)

        if option_type == "call":
                payoff = np.maximum(ST - k, 0.0)
        elif option_type == "put":
                payoff = np.maximum(k - ST, 0.0)
        else:
                raise ValueError("option_type must be 'call' or 'put'.")

        return math.exp(-r * t) * np.mean(payoff)
