import json, sys, warnings
import numpy as np, pandas as pd, yfinance as yf
from scipy import stats
from arch.univariate import ZeroMean, EWMAVariance, StudentsT
from pypfopt import EfficientFrontier, risk_models, expected_returns
warnings.filterwarnings("ignore")

FACTORS = sys.argv[1]; OUT = sys.argv[2]
names = {"BANKBARODA":"Bank of Baroda","BANKINDIA":"Bank of India","MAHABANK":"Bank of Maharashtra",
 "CANBK":"Canara Bank","CENTRALBK":"Central Bank of India","INDIANB":"Indian Bank","IOB":"Indian Overseas Bank",
 "PSB":"Punjab & Sind Bank","PNB":"Punjab National Bank","SBIN":"State Bank of India","UCOBANK":"UCO Bank","UNIONBANK":"Union Bank of India"}
tickers = [k + ".NS" for k in names]
px = yf.download(tickers, start="2020-01-01", end="2025-12-31", auto_adjust=False, progress=False)["Adj Close"].sort_index()
px.columns = [c.replace(".NS","") for c in px.columns]
px = px[sorted(px.columns)]
ret = px.pct_change().dropna()
print("shape", px.shape, ret.shape)
print("check std SBIN", ret.SBIN.std(), "(nb 0.019562)  mean INDIANB", ret.INDIANB.mean(), "(nb 0.001858)")

# weekly-sampled normalized prices (base 100) for the chart
wk = px.resample("W-FRI").last().dropna()
norm = (wk / wk.iloc[0] * 100).round(2)

# rolling 63d annualized vol for all — compact weekly
# EWMA for two stocks
ewma = {}; lam = {}
for s in ["SBIN","UNIONBANK"]:
    r = ret[s] * 100
    res = ZeroMean(r, volatility=EWMAVariance(lam=None), distribution=StudentsT()).fit(disp="off")
    lam[s] = float(res.params["lam"])
    cv = res.conditional_volatility / 100 * np.sqrt(252)
    w = int(np.ceil(np.log(0.1) / np.log(lam[s])))
    roll = ret[s].rolling(w).std(ddof=0) * np.sqrt(252)
    d = pd.DataFrame({"ewma": cv, "roll": roll}).resample("W-FRI").last()
    ewma[s] = {"window": w, "dates": [x.strftime("%Y-%m-%d") for x in d.index],
               "ewma": [None if pd.isna(v) else round(float(v),4) for v in d.ewma],
               "roll": [None if pd.isna(v) else round(float(v),4) for v in d.roll]}
print("lambda", lam, "(nb 0.977710 / 0.927622)")

# return histograms for the two risk stocks
hist = {}
for s in ["SBIN","UNIONBANK"]:
    r = ret[s]; bins = np.linspace(-0.21, 0.21, 85)
    c, e = np.histogram(r.clip(-0.21,0.21), bins=bins)
    df_, loc, sc = stats.t.fit(r)
    hist[s] = {"edges":[round(float(x),4) for x in e], "counts":[int(x) for x in c], "n": len(r),
               "t": {"df":round(float(df_),3),"loc":float(loc),"scale":float(sc)}, "mu": float(r.mean()), "sd": float(r.std())}

# efficient frontier (long-only, sample cov)
mu = expected_returns.mean_historical_return(ret, returns_data=True, compounding=False, frequency=252)
S = risk_models.sample_cov(ret, returns_data=True, frequency=252)
ef = EfficientFrontier(mu, S, weight_bounds=(0,1)); ef.min_volatility()
mr, mv, _ = ef.portfolio_performance()
print("min var", mr, mv, "(nb 0.249377 0.292640)")
front = []
for t in np.linspace(mr, mu.max(), 40):
    try:
        e = EfficientFrontier(mu, S, weight_bounds=(0,1)); e.efficient_return(target_return=t)
        a,b,_ = e.portfolio_performance(); front.append({"vol":round(b,5),"ret":round(a,5),"w":{k:round(v,4) for k,v in e.clean_weights().items() if v>0}})
    except Exception: pass
assets = [{"sym":s,"vol":round(float(np.sqrt(S.loc[s,s])),4),"ret":round(float(mu[s]),4)} for s in mu.index]

corr = ret.corr().round(3)
yearly = (px.resample("YE").last().pct_change()).round(4)
yearly.iloc[0] = (px.resample("YE").last().iloc[0] / px.iloc[0] - 1).round(4)
total = (px.iloc[-1] / px.iloc[0] - 1).round(4)

out = {
 "names": names,
 "syms": list(px.columns),
 "prices": {"dates":[d.strftime("%Y-%m-%d") for d in norm.index], **{s: norm[s].tolist() for s in px.columns}},
 "corr": corr.values.tolist(),
 "yearly": {str(y.year): {s: float(yearly.loc[y, s]) for s in px.columns} for y in yearly.index},
 "total": {s: float(total[s]) for s in px.columns},
 "lastPrice": {s: round(float(px[s].iloc[-1]),2) for s in px.columns},
 "maxDD": {s: round(float((px[s]/px[s].cummax()-1).min()),4) for s in px.columns},
 "ewma": ewma, "lambda": lam, "hist": hist,
 "frontier": front, "assets": assets,
}
json.dump(out, open(OUT,"w"), separators=(",",":"))
print("wrote", OUT)
