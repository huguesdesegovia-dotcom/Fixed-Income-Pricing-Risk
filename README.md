# Fixed-Income-Pricing-Risk

# Fixed Income Pricing & Risk

A Python quantitative finance project implementing bond pricing, yield-to-maturity solving, duration, convexity, yield curve bootstrapping, and portfolio immunization — with an interactive Streamlit dashboard.

## Live Demo

Add your Streamlit Cloud URL here: 🚀 **[Live Demo](https://fixed-income-pricing-risk-xksse5uyfkpv8fwkfm56ys.streamlit.app)**

## Overview

This project prices fixed-coupon bonds, solves for their implied yield, measures their sensitivity to interest rate changes (duration and convexity), reconstructs a spot rate curve from market bond prices (bootstrapping), and computes the portfolio weights needed to immunize a future liability against interest rate risk.

## Features

- **Bond pricing** via discounted cash flows
- **Yield to Maturity (YTM)** solved numerically via bisection
- **Macaulay and Modified Duration**
- **Convexity** (second-order price sensitivity)
- **Yield curve bootstrapping** from market bond prices
- **Portfolio immunization**: weights to match a target duration horizon
- **Automated test suite** (pytest) validating pricing, duration bounds, convexity sign, and immunization consistency
- **Interactive dashboard** (Streamlit + Plotly): pricing & risk, yield curve, and immunization tabs

## Project structure

    Fixed-Income-Pricing-Risk/
    ├── bond_pricing.py     # Pricing, YTM, duration, convexity, immunization
    ├── yield_curve.py       # Spot rate bootstrapping
    ├── dashboard.py           # Interactive Streamlit dashboard
    ├── tests/
    │   └── test_bond_pricing.py  # pytest suite
    ├── requirements.txt
    └── README.md

## The math

### Bond pricing

Price = sum of discounted coupons + discounted face value at maturity, using the market yield.

### Yield to Maturity

No closed-form solution — solved numerically via bisection, finding the yield that reproduces the observed market price.

### Duration

- **Macaulay Duration**: the weighted-average time to receive a bond's cash flows.
- **Modified Duration**: `Macaulay / (1 + yield)`, used to approximate the percentage price change for a small yield move.

### Convexity

The second-order correction to the duration-based price approximation. Always positive for a plain vanilla bond — it benefits the holder in both directions (amplifies gains when yields fall, cushions losses when yields rise).

### Bootstrapping

Extracts a unique spot rate per maturity from a series of market bond prices, solving one new unknown rate at a time using previously solved rates.

### Immunization

Matches a portfolio's duration to a target horizon, so that price risk and reinvestment risk offset each other regardless of rate moves.

## Running the project

Install dependencies: pip3 install -r requirements.txt

Run the tests: pytest

Launch the dashboard: streamlit run dashboard.py

## Tech stack

Python, NumPy, SciPy, pandas, Plotly, Streamlit, pytest

## What I learned

Building this project deepened my understanding of:
- Why bond prices move inversely with yields, and how that link to the discounting mechanic mirrors option pricing
- Why Modified Duration is always slightly below Macaulay Duration
- Why convexity is a structurally favorable property for bondholders
- How bootstrapping solves the limitation of using a single YTM to price bonds against a non-flat yield curve
- How duration matching is used in practice to hedge a portfolio against interest rate risk

## Next steps

- Extend bootstrapping to more maturities and real market data
- Add key rate duration (sensitivity to specific points on the curve)
- Model callable/putable bonds