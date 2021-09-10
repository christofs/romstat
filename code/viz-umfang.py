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
		#print(data.head())
		return data


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "umfang_prozent"]]
	data = data[data["include"] == 1]
	data = data[data["umfang_prozent"] != "N/A"]
	print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"umfang_prozent"])))
	print(data)
	return data,n


def viz(data,n): 
	chart = pygal.Bar(
		style=BlueStyle,
		print_values = True,
		show_legend = True,
    	legend_at_bottom = True,
		legend_at_bottom_columns = 7,
		legend_box_size=40)
	chart.title = "Stellenumfang"
	chart.x_title = "Anteile des Stellenumfangs\n(Daten von romanistik.de, 03/2014-07/2021, Stellen: "+str(n)+")"
	chart.add("25%", data[25]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("50%", data[50]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("65%", data[65]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("75%", data[75]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("80%", data[80]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("90%", data[90]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.add("100%", data[100]/n*100, formatter=lambda x: '{:.1f}%'.format(x))
	chart.render_to_file("romanistik_stellenumfang.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
