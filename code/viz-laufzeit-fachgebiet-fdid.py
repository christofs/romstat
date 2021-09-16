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
		print(data.head())
		return data


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "dauer_cat", "domain_fdid"]]
	data = data[data["include"] == 1]
	data = data[data["domain_fdid"] == 1]
	print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"dauer_cat"])))
	print(data)
	return data,n


def viz(data,n): 
	dark_lighten_style = LightenStyle('#700d17',
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
		legend_box_size=24,
		range = (0,50))
	chart.title = "Vertragslaufzeiten (nur Fachdidaktik)"
	chart.x_title = "Anteile der Vertragslaufzeiten in Prozent (n="+str(n)+")"
	chart.y_title = "Monate"
	chart.x_labels = ["unb.", "66+", "~60", "~48", "~36", "~24", "~12", "1-6"]
	chart.add("Laufzeiten", [data["unb."]/n*100,
							 data["66+"]/n*100,
							 data["~60"]/n*100,
							 data["~48"]/n*100,
							 data["~36"]/n*100,
							 data["~24"]/n*100,
							 data["~12"]/n*100,
							 data["1-6"]/n*100,], formatter=lambda x: '{:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_laufzeit-fachgebiet-fdid.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
