import pandas as pd
import downloader
import csv


if __name__ == "__main__":
	stockNames = []
	with open('june1st_asx200.csv', newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			if(row[0] != "Code" and row[0] != "S&P/ASX 200 Index (1 June 2020)"):
				stockNames.append(row[0])
	print(stockNames)