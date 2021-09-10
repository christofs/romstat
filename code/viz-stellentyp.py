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
		#print(data.head())
		return data


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "pos_string"]]
	data = data[data["include"] == 1]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"pos_string"])))
	print(data)
	return data,n


def viz(data,n): 
	chart = pygal.HorizontalBar(
		style=BlueStyle,
		print_values = True,
		show_legend = False,
    	legend_at_bottom = False,
		legend_at_bottom_columns = 8,
		legend_box_size=32)
	chart.title = "Stellentypen"
	chart.x_title = "Anteile der Stellentypen\n(Daten von romanistik.de, 03/2014-07/2021, Stellen: "+str(n)+")"
	chart.add("LfbA", data["LfbA"]/n*100, formatter=lambda x: 'LfbA {:.1f}%'.format(x))
	chart.add("Lektorat", data["Lektorat"]/n*100, formatter=lambda x: 'Lektorat {:.1f}%'.format(x))
	chart.add("Ratsstelle", data["Ratsstelle"]/n*100, formatter=lambda x: 'Rat {:.1f}%'.format(x))
	chart.add("WMA", data["WMA"]/n*100, formatter=lambda x: 'Wiss. Mitarbeitende {:.1f}%'.format(x))
	chart.add("Promotion", data["Promotion"]/n*100, formatter=lambda x: 'Promotion {:.1f}%'.format(x))
	chart.add("PostDoc", data["PostDoc"]/n*100, formatter=lambda x: 'PostDoc {:.1f}%'.format(x))
	chart.add("Projekt", data["Projekt"]/n*100, formatter=lambda x: 'Projekt {:.1f}%'.format(x))
	chart.add("(Andere)", data["other"]/n*100, formatter=lambda x: 'Andere {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_stellentyp.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
