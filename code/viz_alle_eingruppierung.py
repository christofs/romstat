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
	data = data.loc[:,["include", "gehalt_norm"]]
	data = data[data["include"] == 1]
	data = data[data["gehalt_norm"] != 0]
	print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"gehalt_norm"])))
	print(data)
	return data,n


def viz(data,n): 
	dark_lighten_style = LightenStyle('#063d1e',
		step=10, 
		font_family="FreeSans",
		label_font_size = 12,
		major_label_font_size = 12,
		value_label_font_size = 12,
		value_font_size = 10,
		title_font_size = 16)
	chart = pygal.HorizontalBar(
		style=dark_lighten_style,
		print_values = True,
		show_legend = False,
    	legend_at_bottom = True,
		legend_at_bottom_columns = 7,
		legend_box_size=40)
	chart.title = "Eingruppierung (ohne E13 = 93%)"
	chart.x_title = "Anteile der Gehaltsgruppen in Prozent (n="+str(n)+")"
	chart.y_title = "Gehaltsgruppen"
	chart.x_labels = ["A15", "E15", "A14", "E14", "A13", "E12", "E11"]
	chart.add("Gehaltsgruppen", [data["A15"]/n*100,
								 data["E15"]/n*100,
								 data["A14"]/n*100,
								 data["E14"]/n*100,
								 data["A13"]/n*100,
								 0,
								 data["E11"]/n*100,], formatter=lambda x: '{:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_alle-eingruppierung.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
