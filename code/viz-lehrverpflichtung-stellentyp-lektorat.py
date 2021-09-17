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
from pygal.style import LightenStyle


def get_data(): 
	with open("../data/romanistik-stellen_datensatz_2014-2021.csv", "r", encoding="utf8") as infile: 
		data = pd.read_csv(infile, sep="\t")
		#print(data.head())
		return data


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "sws_äqv", "pos_string"]]
	data = data[data["include"] == 1]
	data = data[data["pos_string"] == "Ratsstelle"]
	data = data[data["sws_äqv"] != "N/A"]
	data = data[data["sws_äqv"] != 0]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"sws_äqv"])))
	for i in range(0,26):
		try: 
			print(data[str(i)])
		except: 
			data[str(i)] = 0
	print(data)
	return data,n


def viz(data,n): 
	dark_lighten_style = LightenStyle('#7724a3',
		step=10, 
		font_family="FreeSans",
		label_font_size = 12,
		major_label_font_size = 12,
		value_label_font_size = 12,
		value_font_size = 12,
		title_font_size = 16)
	chart = pygal.HorizontalBar(
		style=dark_lighten_style,
		print_values = True,
		show_legend = False,
    	legend_at_bottom = True,
		legend_at_bottom_columns = 9,
		legend_box_size=24)
	chart.title = "Lehrverpflichtung (nur Lektorat)"
	chart.x_title = "Anteile der Lehrverpflichtungen in Prozent (n="+str(n)+")"
	chart.y_title = "SWS (Vollzeit-Äquivalente)"
	chart.x_labels = ["25", "24", "23", "22", "21", "20", "19", "18", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"]
	chart.add("Laufzeiten", [data["25"]/n*100,
							 data["14"]/n*100,
							 data["23"]/n*100,
							 data["22"]/n*100,
							 data["21"]/n*100,
							 data["20"]/n*100,
							 data["19"]/n*100,
							 data["18"]/n*100,
							 data["17"]/n*100,
							 data["16"]/n*100,
							 data["15"]/n*100,
							 data["14"]/n*100,
							 data["13"]/n*100,
							 data["12"]/n*100,
							 data["11"]/n*100,
							 data["10"]/n*100,
							 data["9"]/n*100,
							 data["8"]/n*100,
							 data["7"]/n*100,
							 data["6"]/n*100,
							 data["5"]/n*100,
							 data["4"]/n*100,
							 data["3"]/n*100,
							 data["2"]/n*100,
							 data["1"]/n*100,
							 data["0"]/n*100], formatter=lambda x: '{:.0f}%'.format(x))
	chart.render_to_file("../img/romanistik_lehrverpflichtung-stellentyp-rat.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
