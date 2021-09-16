import re
from os.path import join
import glob
import os
import pandas as pd
from datetime import date
import pygal
from pygal.style import BlueStyle
from pygal.style import DarkGreenBlueStyle
from pygal.style import TurquoiseStyle
from pygal.style import CleanStyle
from collections import Counter


def get_data(): 
	with open("../data/romanistik-stellen-datensatz_2021-09-09.csv", "r", encoding="utf8") as infile: 
		data = pd.read_csv(infile, sep="\t")
		print(data.head())
		return data



def viz_dauer(data): 
	# Filter down to useable data
	dauerdata = data.loc[:,["jahr", "dauer_norm", "include"]]
	dauerdata = dauerdata[dauerdata["dauer_norm"].apply(lambda x: str(x).isdigit())]
	dauerdata = dauerdata[dauerdata["jahr"].apply(lambda x: str(x).isdigit())]
	dauerdata = dauerdata[dauerdata["include"] == 1]
	#print(dauerdata.head())
	datenpunktesumme = dauerdata.shape[0]
	print("Anzahl der Datenpunkte", datenpunktesumme)
	dauerdata = dauerdata.groupby("jahr")
	
	# Make boxplot (distribution)
	boxplot = pygal.Box(box_mode="tukey", 
					    style=CleanStyle,
					    legend_at_bottom = True,
					    legend_at_bottom_columns = 8,
					    truncate_legend=5)
	boxplot.title = "Vertragsdauer pro Jahr\n(Daten von romanistik.de, 03/2014-07/2021, Stellen: "+str(datenpunktesumme)+")"
	boxplot.x_title = "Jahre"
	boxplot.y_title = "Vertragsdauer in Monaten\n(120=unbefristet)"
	for year,group in dauerdata:
		dauerdatayear = list(group["dauer_norm"].astype(int)) 
		label = str(year) + " (" + str(len(dauerdatayear)) + " Stellen)"
		boxplot.add(label, dauerdatayear)
	boxplot.render_to_file("romanistik_jahr-dauer_boxplot.svg")
	
	# Prepare data for stacked barchart
	yearlypercentages = {}
	#categories = ["1-11", "12-23", "24-35", "36-47", "48-59", "60-71", "72+", "unbefristet"]
	categories = ["1-6", "~12", "~24", "~36", "~48", "~60", "~72", "78+", "unb."]
	yearlypercentages["cats"] = categories
	for year,group in dauerdata: 
		dauerdatayear = list(group["dauer_norm"].astype(int)) 
		numitems = len(dauerdatayear)
		label = str(year) + " (" + str(numitems) + " Stellen)"
		#print(label)
		dauerdatayearbinned = []
		for item in dauerdatayear: 
			if item > 0 and item < 6: 
				dauerdatayearbinned.append(categories[0])
			if item >= 6 and item < 18: 
				dauerdatayearbinned.append(categories[1])
			if item >= 18 and item < 30: 
				dauerdatayearbinned.append(categories[2])
			if item >= 30 and item < 42: 
				dauerdatayearbinned.append(categories[3])
			if item >= 42 and item < 54: 
				dauerdatayearbinned.append(categories[4])
			if item >= 54 and item < 66: 
				dauerdatayearbinned.append(categories[5])
			if item >= 66 and item < 78: 
				dauerdatayearbinned.append(categories[6])
			if item >= 78 and item < 119: 
				dauerdatayearbinned.append(categories[7])
			if item >= 119: 
				dauerdatayearbinned.append(categories[8])
		dauerdatayearbinned = dict(Counter(dauerdatayearbinned))
		#print(dauerdatayearbinned)
		for item in dauerdatayearbinned: 
			dauerdatayearbinned[item] = dauerdatayearbinned[item] / numitems * 100
		#print(dauerdatayearbinned)
		for category in categories: 
			try: 
				dauerdatayearbinned[category]
			except: 
				dauerdatayearbinned[category] = 0 
		#print(dauerdatayearbinned)
		percentages = []
		for category in categories:
			percentages.append(dauerdatayearbinned[category])
		#print(percentages)
		yearlypercentages[year] = percentages
	yearlypercentages = pd.DataFrame(yearlypercentages)
	yearlypercentages.set_index("cats", inplace=True)
	yearlypercentages = yearlypercentages.T
	#print(yearlypercentages)

	# Make stacked barchart (proportions)
	barchart = pygal.StackedBar(style=BlueStyle,
    				     legend_at_bottom = False,
					     legend_at_bottom_columns = 5,
					     legend_box_size=24,
					     truncate_legend=5)
	barchart.title = "Anteile der Vertragsdauern pro Jahr (n="+str(datenpunktesumme)+")"
	barchart.x_title = "Jahre"
	barchart.y_title = "Anteile (Prozent) der Gruppen von Vertragsdauern"
	barchart.x_labels = map(str, range(2014, 2022))
	for row in yearlypercentages: 
		label = yearlypercentages[row].name
		data = list(yearlypercentages[row])
		#print(label, data)		
		barchart.add(label, data, formatter=lambda x: '{:.1f}%'.format(x))
	barchart.render_to_file("../img/romanistik_jahr-dauer.svg")
			
			


def main(): 
	data = get_data()
	viz_dauer(data)
	

main()	
