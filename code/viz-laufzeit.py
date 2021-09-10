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


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "dauer_cat"]]
	data = data[data["include"] == 1]
	print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"dauer_cat"])))
	print(data)
	return data,n


def viz(data,n): 
	chart = pygal.HorizontalBar(
		style=BlueStyle,
		print_values = True,
		show_legend = False,
    	legend_at_bottom = True,
		legend_at_bottom_columns = 9,
		legend_box_size=24)
	chart.title = "Vertragslaufzeiten"
	chart.x_title = "Anteile der Nennungen verschiedener Vertragslaufzeiten\n(Daten von romanistik.de, 03/2014-07/2021, Stellen: "+str(n)+")"
	chart.add("1-6", data["1-6"]/n*100, formatter=lambda x: '1-6 {:.1f}%'.format(x))
	chart.add("~12", data["~12"]/n*100, formatter=lambda x: '~12 {:.1f}%'.format(x))
	chart.add("~24", data["~24"]/n*100, formatter=lambda x: '~24 {:.1f}%'.format(x))
	chart.add("~36", data["~36"]/n*100, formatter=lambda x: '~36 {:.1f}%'.format(x))
	chart.add("~48", data["~48"]/n*100, formatter=lambda x: '~48 {:.1f}%'.format(x))
	chart.add("~60", data["~60"]/n*100, formatter=lambda x: '~60 {:.1f}%'.format(x))
	chart.add("~72", data["~72"]/n*100, formatter=lambda x: '~72 {:.1f}%'.format(x))
	chart.add("78+", data["78+"]/n*100, formatter=lambda x: '78+ {:.1f}%'.format(x))
	chart.add("unb.", data["unb."]/n*100, formatter=lambda x: 'unb. {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_befristungsdauer.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
