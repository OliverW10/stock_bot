# 7LAPJHZTCXNLYF6H
# alpha vantage key (could get to work with asx)
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import json
import time

def getStockPrice(name):
	ticker = yf.Ticker(name)
	his = ticker.history("1d", "1m")
	return his["Close"][-1]

def downloadStockHistory(name, period = "1mo", interval = "1h"):
	ticker = yf.Ticker(name)
	his = ticker.history(period, interval)
	his.to_pickle("histories/"+name+".pkl")
	return his

def getStockHistory(stockName):
	return pd.read_pickle("histories/"+stockName+".pkl")

def updateStockHistory(stockName, period = "1mo", interval = "1d", maxOutdated = 3600): # maxOutdated = 0 for force download
	print(stockName+" ", end = "")
	with open("chacheData.json", "r") as f:
		chacheData = json.loads(f.read())

		try: # will error if the stock has never been downloaded before
			if abs(chacheData[stockName]["time"] - time.time()) < maxOutdated and chacheData[stockName]["interval"] == interval and chacheData[stockName]["period"] == period: # if the exact data is chached
				print("used chached")
				return getStockHistory(stockName)
			else:
				print("updated old data")
		except:
			print("got first time")

	chacheData[stockName] = {"time":time.time(), "interval": interval, "period": period}

	with open("chacheData.json", "w") as f:
		# print(json.dumps(chacheData))
		f.write(json.dumps(chacheData))

	return downloadStockHistory(stockName, period, interval)

if __name__ == "__main__":
	test = updateStockHistory("XRO.AX", "1mo", "1d")
	print(test["Close"].values)
	# plt.plot(test["Open"])
	# plt.show()
