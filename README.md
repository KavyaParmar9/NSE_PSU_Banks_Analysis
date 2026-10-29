# Quantitative Financial Analysis — NIFTY PSU Bank

A collaborative academic project for the **SC453 Quantitative Financial Analysis** course, using Python and Google Colab to study financial returns, measure market risk, model volatility, and optimize portfolios of Indian Public Sector Undertaking (PSU) bank stocks.

The notebook contains both the code and interpretations of the results, connecting quantitative finance concepts with historical market data.

## Project Overview

This project analyzes the NIFTY PSU Bank Index and its 12 current constituent stocks using daily adjusted closing prices from January 2020 to December 2025.

The objective is to apply statistical and quantitative finance methods to understand stock return behavior, estimate potential losses, examine changing volatility, and evaluate portfolio allocations under different risk assumptions.

## Key Analyses

### 1. Data Collection and Exploratory Analysis
- Retrieved historical adjusted closing prices using Yahoo Finance and `yfinance`.
- Examined data types, duplicate dates, missing values, and invalid prices.
- Calculated daily simple returns for the constituent stocks.
- Analyzed descriptive statistics, return distributions, annualized volatility, and correlations.
- Visualized price movements and return distributions to identify patterns in the data.

### 2. Risk Measurement: VaR and Expected Shortfall
- Estimated **Value at Risk (VaR)** at 95% and 99% confidence levels.
- Compared historical, Student's t-distribution-based, and parametric approaches.
- Calculated Expected Shortfall (ES) to examine average losses in the tail beyond the VaR threshold.
- Compared risk estimates for State Bank of India (SBI) and Union Bank of India across the 2020–2022 and 2023–2025 periods.
- Examined a March 2020 stress scenario alongside the 2023–2025 observations.

### 3. Volatility Estimation and Forecasting
- Applied an Exponentially Weighted Moving Average (EWMA) approach to estimate changing volatility.
- Estimated the EWMA decay parameter using maximum likelihood estimation.
- Examined the relationship between EWMA variance estimates and subsequent squared returns.
- Compared EWMA volatility with rolling-window volatility estimates.

### 4. Portfolio Optimization
- Constructed minimum-variance portfolios using historical return and covariance estimates.
- Compared long-only portfolios with portfolios that permit short selling.
- Explored efficient frontiers to examine the relationship between expected return and portfolio risk.
- Compared portfolio allocations using different covariance estimation methods, including sample covariance, EWMA, shrinkage, and sparse covariance estimates.

### 5. Factor and Beta Analysis
- Explored CAPM beta estimation to examine stock sensitivity to market returns.
- Included four-factor regression analysis to study stock returns in relation to market and other factor returns.

*The factor-regression results are still subject to validation, including checks on return units, factor-data scales, and model interpretation.*

## Technologies and Libraries

- **Language:** Python
- **Environment:** Google Colab, Jupyter Notebook
- **Data handling:** Pandas, NumPy
- **Data retrieval:** yfinance
- **Statistical analysis:** SciPy, Statsmodels, arch
- **Portfolio optimization:** PyPortfolioOpt
- **Visualization:** Matplotlib, Seaborn

## Dataset

The primary dataset consists of daily adjusted closing prices for 12 current NIFTY PSU Bank constituent stocks over the January 2020–December 2025 period.

Historical prices are retrieved through Yahoo Finance using `yfinance`. The factor-analysis section additionally reads the following CSV file:

`2025-12_FourFactors_and_Market_Returns_Daily_SurvivorshipBiasAdjusted.csv`

This file must be available in the Colab session, or its path must be updated, to execute the corresponding factor-analysis section.

## How to Run

1. Open `G7_SC453_project.ipynb` in [Google Colab](https://colab.research.google.com/).
2. Install any required libraries that are not already available:

   ```python
   !pip install yfinance arch PyPortfolioOpt statsmodels scipy seaborn
   ```

3. Ensure that the factor-data CSV is uploaded if you want to execute the factor-regression analysis.
4. Run the notebook cells in order, from data retrieval and cleaning through risk measurement, volatility modelling, and portfolio optimization.
5. Review the interpretations, tables, and visualizations alongside the corresponding code.

An active internet connection is required to retrieve historical price data through Yahoo Finance.

## Project Structure

```text
Quantitative-Financial-Analysis/
├── G7_SC453_project.ipynb
├── 2025-12_FourFactors_and_Market_Returns_Daily_SurvivorshipBiasAdjusted.csv
└── README.md
```


## Limitations and Considerations

- Historical returns and risk estimates describe the selected data period and do not guarantee future performance.
- Historical VaR and parametric VaR rely on different assumptions and may behave differently during extreme market conditions.
- Portfolio optimization is sensitive to expected-return and covariance estimates.
- Using the current constituent list across historical periods can introduce survivorship bias when evaluating past market behavior.
- Volatility forecasts and factor regressions require validation before their outputs can support broader conclusions.

## Project Status

**Ongoing academic project.**

The notebook documents the analytical workflow, code, and interpretations. Risk-model validation, volatility forecast assessment, and factor-regression checks remain important parts of the ongoing work.

## Contributors

Group 7 — SC453 Quantitative Financial Analysis.


## Disclaimer

This project is intended for academic and educational purposes only. It is not financial advice and should not be used as the sole basis for investment decisions.
