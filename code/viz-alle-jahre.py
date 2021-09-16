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
	data = data.loc[:,["include", "jahr"]]
	data = data[data["include"] == 1]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(list(data.loc[:,"jahr"])))
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
	chart = pygal.Bar(
		style=dark_lighten_style,
		print_values = True,
		show_legend = False,
    	legend_at_bottom = False,
		legend_at_bottom_columns = 8,
		legend_box_size=32)
	chart.title = "Stellenausschreibungen pro Jahr"
	chart.x_title = "Anzahl der Stellenausschreibungen pro Jahr (n="+str(n)+")"
	chart.y_title = "Anzahl"
	chart.x_labels = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]
	chart.add("Jahre", [data[2021],
					    data[2020],
					    data[2019],
					    data[2018],
					    data[2017],
					    data[2016],
					    data[2015],
					    data[2014],], formatter=lambda x: '{:.0f}'.format(x))
	chart.render_to_file("../img/romanistik_alle-jahre.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
