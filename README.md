Black-Scholes & Implied Volatility Project

This project provides a toolkit for pricing and analyzing options using the Black-Scholes model and market-implied volatilities.

Features

Data Fetching: Retrieves live options chain data for user-selected equities via yfinance.

Options Pricing: Computes theoretical option prices (calls/puts) for a chosen strike, expiry, and date using the Black-Scholes model.

Greeks Calculation: Evaluates option sensitivities (Δ, Γ, Θ, ρ, vega) for all available contracts on a given date.

Implied Volatility Estimation: Extracts implied volatilities using the Brent root-finding method, ensuring robust convergence.

Implied Volatility Surface Plotting: Visualizes volatility as a function of moneyness and time-to-expiry, enabling 3D inspection of skew and term structure.

Notes

Implied volatility plots may occasionally appear incomplete or noisy, as yfinance provides patchy or missing options data at certain strikes/expiries.

Results should be interpreted with caution, particularly for illiquid contracts or deep OTM/ITM strikes.

Requirements

Python 3.9+

numpy, pandas, scipy, matplotlib, yfinance

Usage

Select a stock ticker.

Specify option type, strike, and expiry date.

Compute prices/Greeks and/or generate an implied volatility surface.
