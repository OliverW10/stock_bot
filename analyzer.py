import pandas as pd
import downloader
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def getChange(prices): # takes an array of prices and computes the change each day
	change = [0]
	for i in range(1, len(prices)):
		change.append((prices[i]-prices[i-1])/prices[i])
	return change

def consequtiveGrowth(vals, changes):
	if changes[-2] > 0 and abs(changes[-1]) < 0.1:
		return changes[-1]
	else:
		return 0

def reverseGrowth(vals, changes):
	if changes[-2] < 0: #  and abs(changes[-1]) < 0.1
		return changes[-1]
	else:
		return False

def belowAvg(vals, changes):
	avg = prevAvg(vals[:-1])
	if vals[-2] < avg: #  and abs(vals[-1]) < 0.1
		return changes[-1]
	else:
		return False

def prevAvg(vals, cap = 7):
	# print(vals[-cap:])
	return sum(vals[-cap:]) / len(vals[-cap:])


def avgFor(req, vals, changes):
	# all datapoints on the set that meet req
	total = 0
	num = 0
	for i in range(2, len(vals)):
		val = req(vals[:i], changes[:i])
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
	print(len(stockNames))
	#stockNames = stockNames[0:50]
	# print(stockNames)
	changes = {}
	closes = {}
	avg = []
	bel = []
	rev = []
	for sym in stockNames:
		data = downloader.updateStockHistory(sym+".AX", "3mo", "1d", 100000)
		closes[sym] = data["Close"].values.tolist()
		changes[sym] = getChange(closes[sym])
		rev.append(avgFor(reverseGrowth, closes[sym], changes[sym]))
		bel.append(avgFor(belowAvg, closes[sym], changes[sym]))
		avg.append(sum(changes[sym])/len(changes[sym]))
		print("reverse growth: "+str(rev[-1]))
		print("below average:  "+str(bel[-1]))
		print("all:            "+str(avg[-1]))

		weekAvg = []
		for i in range(2, len(closes[sym])):
			weekAvg.append(prevAvg(closes[sym][:i]))

		# plt.plot(weekAvg)
		# plt.plot(closes[sym])
		# plt.show()



	x = np.arange(len(stockNames))  # the label locations
	width = 0.3  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - width, avg, width, label='All')
	rects2 = ax.bar(x + width, bel, width, label='Buy when below 7 day average')
	rects3 = ax.bar(x, rev, width, label='By when fall')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Average change')
	ax.set_title('Average change by stock for techniques')
	ax.set_xticks(x)
	ax.set_xticklabels(stockNames)
	ax.legend()


	def autolabel(rects):
	    """Attach a text label above each bar in *rects*, displaying its height."""
	    for rect in rects:
	        height = rect.get_height()
	        # ax.annotate('{}'.format(height),
	        #             xy=(rect.get_x() + rect.get_width() / 2, height),
	        #             xytext=(0, 3),  # 3 points vertical offset
	        #             textcoords="offset points",
	        #             ha='center', va='bottom')


	autolabel(rects1)
	autolabel(rects2)
	autolabel(rects3)

	fig.tight_layout()

	print("\n\n")
	print("avg total: "+str(sum(avg)/len(avg)))
	print("bel total: "+str(sum(bel)/len(bel)))
	print("rev total: "+str(sum(rev)/len(rev)))

	plt.show()