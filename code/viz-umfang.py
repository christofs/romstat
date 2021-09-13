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
    	legend_at_bottom = True,
		legend_at_bottom_columns = 7,
		legend_box_size=40)
	chart.title = "Stellenumfang"
	chart.x_title = "Anteile des Stellenumfangs in Prozent (n="+str(n)+")"
	chart.add("25%", data[25]/n*100, formatter=lambda x: '~25%: {:.1f}%'.format(x))
	chart.add("50%", data[50]/n*100, formatter=lambda x: '~50%: {:.1f}%'.format(x))
	chart.add("65%", data[65]/n*100, formatter=lambda x: '~65%: {:.1f}%'.format(x))
	chart.add("75%", data[75]/n*100, formatter=lambda x: '~75%: {:.1f}%'.format(x))
	chart.add("80%", data[80]/n*100, formatter=lambda x: '~80%: {:.1f}%'.format(x))
	chart.add("90%", data[90]/n*100, formatter=lambda x: '~90%: {:.1f}%'.format(x))
	chart.add("100%", data[100]/n*100, formatter=lambda x: '~100%: {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_stellenumfang.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
