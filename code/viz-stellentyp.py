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
	dark_lighten_style = LightenStyle('#004466',
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
	chart.title = "Stellentypen"
	chart.x_title = "Anteile der Stellentypen in Prozent (n="+str(n)+")"
	chart.add("LfbA", data["LfbA"]/n*100, formatter=lambda x: 'LfbA {:.1f}%'.format(x))
	chart.add("Lektorat", data["Lektorat"]/n*100, formatter=lambda x: 'Lektorat {:.1f}%'.format(x))
	chart.add("Ratsstelle", data["Ratsstelle"]/n*100, formatter=lambda x: 'Rat {:.1f}%'.format(x))
	chart.add("WMA", data["WMA"]/n*100, formatter=lambda x: 'WMA allg. {:.1f}%'.format(x))
	chart.add("Promotion", data["Promotion"]/n*100, formatter=lambda x: 'WMA (Promotion) {:.1f}%'.format(x))
	chart.add("PostDoc", data["PostDoc"]/n*100, formatter=lambda x: 'WMA (PostDoc) {:.1f}%'.format(x))
	chart.add("Projekt", data["Projekt"]/n*100, formatter=lambda x: 'WMA (Projekt) {:.1f}%'.format(x))
	chart.add("Fellow", data["Projekt"]/n*100, formatter=lambda x: 'Fellowship {:.1f}%'.format(x))
	chart.add("(Andere)", data["other"]/n*100, formatter=lambda x: 'Andere {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_stellentyp.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
