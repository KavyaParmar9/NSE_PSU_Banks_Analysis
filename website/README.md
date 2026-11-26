# PSU Bank Ledger: project website

An interactive, single-page website that presents the results of the NIFTY PSU Bank analysis: rebased price paths, the constituent summary table, correlations, VaR and Expected Shortfall, the March 2020 stress test, EWMA volatility, the efficient frontier, minimum-variance weights and factor betas.

**This website was designed and built by Kavya Parmar.** The other group members contributed to the original project notebook (`G7_SC453_project.ipynb`) submitted for SC453 only. They were not involved in the website.

## Viewing it

Open `index.html` in a browser. It is a self-contained page with no build step; fonts load from Google Fonts.

To publish it with GitHub Pages, enable Pages for this repository and point it at this branch's `/website` folder (or copy `index.html` to the publishing root).

## Files

| File | Purpose |
|---|---|
| `index.html` | The finished page, with chart data embedded |
| `template.html` | The same page with a `/*DATA*/null` placeholder where the data goes |
| `series.json` | Chart series (rebased weekly prices, EWMA and rolling volatility, return histograms, efficient frontier, correlations) |
| `build_data.py` | Re-downloads prices with `yfinance` and regenerates `series.json` |

## Rebuilding the data

```bash
pip install pandas numpy scipy yfinance arch PyPortfolioOpt
python build_data.py ../2025-12_FourFactors_and_Market_Returns_Daily_SurvivorshipBiasAdjusted.csv series.json
python -c "t=open('template.html').read(); open('index.html','w').write(t.replace('/*DATA*/null', open('series.json').read()))"
```

Then wrap the result in a standard `<!doctype html>` / `<head>` / `<body>` skeleton as in the committed `index.html`.

The script reproduces the notebook's results: SBIN daily standard deviation 0.019562, EWMA λ of 0.97771 (SBIN) and 0.92762 (UNIONBANK), and a long-only minimum-variance portfolio with 24.94% expected return and 29.26% volatility. Tables of VaR/ES, regression output, portfolio weights and factor betas are taken directly from the notebook's outputs.
