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
	data = data.loc[:,["include", "umfang_sws", "umfang_prozent"]]
	data = data[data["include"] == 1]
	data = data[data["umfang_prozent"] != 0]
	data = data[data["umfang_sws"] != 0]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data1 = list(data.loc[:,"umfang_sws"])
	data2 = list(data.loc[:,"umfang_prozent"])
	data3 = [round((i / j)*100) for i, j in zip(data1, data2) if j !=0]
	data = dict(Counter(data3))
	print(data)
	return data,n


def viz(data,n): 
	dark_lighten_style = LightenStyle('#063d1e',
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
	chart.title = "Lehrverpflichtung"
	chart.x_title = "Anzahl der SWS auf volle Stelle hochgerechnet (n="+str(n)+")"
	chart.y_title = "SWS"
	chart.x_labels = ["24", "23", "22", "21", "20", "19", "18", "17", "16",
					  "15", "14", "13", "12", "11", "10", "9", "8", "7",
					   "6", "5", "4", "3", "2", "1"]
	chart.add("SWS", [data[24],
					  data[23],
					  0,
					  0,
					  data[20],
					  0,
					  data[18],
					  data[17],
					  data[16],
					  data[15],
					  data[14],
					  data[13],
					  data[12],
					  0,
					  data[10],
					  data[9],
					  data[8],
					  data[7],
					  data[6],
					  data[5],
					  data[4],
					  data[3],
					  data[2],
					  0], formatter=lambda x: '{:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_alle-sws.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
