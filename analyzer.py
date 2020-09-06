import pandas as pd
import downloader
import csv
import matplotlib.pyplot as plt

def getChange(prices): # takes an array of prices and computes the change each day
	change = [0]
	for i in range(1, len(prices)):
		change.append((prices[i]-prices[i-1])/prices[i])
	return change

def consequtiveGrowth(prevDay, today):
	if prevDay > 0 and abs(today) < 0.1:
		return today
	else:
		return 0

def reverseGrowth(prevDay, today):
	if prevDay < 0 and abs(today) < 0.1:
		return today
	else:
		return False

def avgFor(req, data):
	# all datapoints on the set that meet req
	total = 0
	num = 0
	for i in range(len(data)):
		val = req(data[i-1], data[i])
		if not val == False:
			total += val
			num += 1
	return total/num

if __name__ == "__main__":
	stockNames = []
	with open('june1st_asx200.csv', newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			if(row[0] != "Code" and row[0] != "S&P/ASX 200 Index (1 June 2020)"):
				stockNames.append(row[0])
	stockNames = stockNames[0:20]
	# print(stockNames)
	changes = {}
	for sym in stockNames:
		data = downloader.updateStockHistory(sym+".AX", "1y", "1d", 10000)
		changes[sym] = getChange(data["Close"].values)
		print(avgFor(reverseGrowth, changes[sym]))

	
	# plt.plot(changes["ABP"])
	# plt.show()

	continuance = [] # a number to quantify how much a days change is predicted by the previous day