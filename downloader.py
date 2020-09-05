# 7LAPJHZTCXNLYF6H
# alpha vantage key (could get to work with asx)
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def getStockPrice(name):
	ticker = yf.Ticker(name)
	his = ticker.history("1d", "1m")
	return his["Close"][-1]

def downloadStockHistory(name, period = "1mo", interval = "1h"):
	ticker = yf.Ticker(name)
	his = ticker.history(period, interval)
	his.to_pickle("histories/"+name+".pkl")
	return his

def loadStockHistory(stockName):
	return pd.read_pickle("histories/"+stockName+".pkl")

if __name__ == "__main__":
	test2 = downloadStockHistory("XRO.AX", "1mo", "1d")
	plt.plot(test2["Open"])
	plt.show()
