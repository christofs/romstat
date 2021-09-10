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
	with open("romanistik-stellen-datensatz_2021-09-09.csv", "r", encoding="utf8") as infile: 
		data = pd.read_csv(infile, sep="\t")
		print(data.head())
		return data


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "dauer_norm", "position_string"]]
	data = data[data["include"] == 1]
	data = data[data["dauer_norm"] == 120]	
	print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"position_string"])))
	print(data)
	return data,n


def viz(data,n): 
	chart = pygal.Bar(
		style=BlueStyle,
		print_values = True,
		show_legend = True,
    	legend_at_bottom = True,
		legend_at_bottom_columns = 5,
		legend_box_size=40)
	chart.title = "Stellentypen bei unbefristeten Stellen"
	chart.x_title = "Anzahl der Nennung von Stellentypen\n(Daten von romanistik.de, 03/2014-07/2021, Stellen: "+str(n)+")"
	types = ["LfbA", "Lektorat", "Ratsstelle", "WMA", "other"]
	chart.add("LfbA", data["LfbA"]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("Lektorat", data["Lektorat"]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("Ratsstelle", data["Ratsstelle"]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("WMA", data["WMA"]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("(Andere)", data["other"]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.render_to_file("romanistik_unbefristete-stellentypen.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
