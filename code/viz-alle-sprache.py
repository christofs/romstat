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
	data = data.loc[:,["include", "lang_string"]]
	data = data[data["include"] == 1]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"lang_string"])))
	print(data)
	return data,n


def viz(data,n): 
	dark_lighten_style = LightenStyle('#8f0a94',
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
    	legend_at_bottom = False,
		legend_at_bottom_columns = 8,
		legend_box_size=32)
	chart.title = "Sprachen"
	chart.x_title = "Anteile der genannten Sprachen in Prozent (n="+str(n)+")"
	chart.y_title = "Sprachen"
	chart.x_labels = ["sprachüb.", "mehrere", "Port.", "Ital.", "Span.", "Franz."]
	chart.add("Sprachen", [data["other"]/n*100,
							   data["mult"]/n*100,
							   data["por"]/n*100,
							   data["ita"]/n*100,
							   data["spa"]/n*100,
							   data["frz"]/n*100], formatter=lambda x: '{:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_alle-sprachen.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	