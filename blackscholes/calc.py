import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def d1_calc(S, K, T, r, sigma):
    return (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))

def d2_calc(S, K, T, r, sigma):
    return d1_calc(S, K, T, r, sigma) - sigma * np.sqrt(T)

def black_scholes(S, K, T, r, sigma, option_type="calls"):
    d1 = d1_calc(S, K, T, r, sigma)
    d2 = d2_calc(S, K, T, r, sigma)
    if option_type == "calls":
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    elif option_type == "puts":
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    
def delta_calc(S, K, T, r, sigma, option_type="calls"):
    d1 = d1_calc(S, K, T, r, sigma)
    if option_type == "calls":
        return norm.cdf(d1)
    elif option_type == "puts":
        return -norm.cdf(-d1)
    
def gamma_calc(S, K, T, r, sigma):
    d1 = d1_calc(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def vega_calc(S, K, T, r, sigma):
    d1 = d1_calc(S, K, T, r, sigma)
    return S * norm.pdf(d1) * np.sqrt(T)*0.01

def theta_calc(S, K, T, r, sigma, option_type="calls"):
    d1 = d1_calc(S, K, T, r, sigma)
    d2 = d2_calc(S, K, T, r, sigma)
    if option_type == "calls":
        return (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    elif option_type == "puts":
        return (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    
def rho_calc(S, K, T, r, sigma, option_type="calls"):
    d2 = d2_calc(S, K, T, r, sigma)
    if option_type == "calls":
        return (K * T * np.exp(-r * T) * norm.cdf(d2) )/ 100
    elif option_type == "puts":
        return (-K * T * np.exp(-r * T) * norm.cdf(-d2)) / 100
    
def implied_volatility(S, K, T, r, market_price, option_type="calls"):
    def objective_function(sigma):
        return black_scholes(S, K, T, r, sigma, option_type) - market_price
    
    try:
        return brentq(objective_function, 1e-6, 5.0)
    except ValueError:
        return np.nan  # If no solution found