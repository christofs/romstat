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
	chart.title = "Lehrverpflichtung"
	chart.x_title = "Anzahl der SWS auf volle Stelle hochgerechnet (n="+str(n)+")"
	try: 
		chart.add("1", data[1], formatter=lambda x: '1 SWS: {:.1f}%'.format(x))
	except: 
		chart.add("1", 0, formatter=lambda x: '1 SWS: {:.1f}%'.format(x))
	chart.add("2", data[2]/n*100, formatter=lambda x: '2 SWS: {:.1f}%'.format(x))
	chart.add("3", data[3]/n*100, formatter=lambda x: '3 SWS: {:.1f}%'.format(x))
	chart.add("4", data[4]/n*100, formatter=lambda x: '4 SWS: {:.1f}%'.format(x))
	chart.add("5", data[5]/n*100, formatter=lambda x: '5 SWS: {:.1f}%'.format(x))
	chart.add("6", data[6]/n*100, formatter=lambda x: '6 SWS: {:.1f}%'.format(x))
	chart.add("7", data[7]/n*100, formatter=lambda x: '7 SWS: {:.1f}%'.format(x))
	chart.add("8", data[8]/n*100, formatter=lambda x: '8 SWS: {:.1f}%'.format(x))
	chart.add("9", data[9]/n*100, formatter=lambda x: '9 SWS: {:.1f}%'.format(x))
	chart.add("10", data[10]/n*100, formatter=lambda x: '10 SWS: {:.1f}%'.format(x))
	try: 
		chart.add("11", data[11]/n*100, formatter=lambda x: '11 SWS: {:.1f}%'.format(x))
	except: 
		chart.add("11", 0, formatter=lambda x: '11 SWS: {:.1f}%'.format(x))

	chart.add("12", data[12]/n*100, formatter=lambda x: '12 SWS: {:.1f}%'.format(x))
	chart.add("13", data[13]/n*100, formatter=lambda x: '13 SWS: {:.1f}%'.format(x))
	chart.add("14", data[14]/n*100, formatter=lambda x: '14 SWS: {:.1f}%'.format(x))
	chart.add("15", data[15]/n*100, formatter=lambda x: '15 SWS: {:.1f}%'.format(x))
	chart.add("16", data[16]/n*100, formatter=lambda x: '16 SWS: {:.1f}%'.format(x))
	chart.add("17", data[17]/n*100, formatter=lambda x: '17 SWS: {:.1f}%'.format(x))
	chart.add("18", data[18]/n*100, formatter=lambda x: '18 SWS: {:.1f}%'.format(x))
	try: 
		chart.add("19", data[19]/n*100, formatter=lambda x: '19 SWS: {:.1f}%'.format(x))
	except: 
		chart.add("19", 0, formatter=lambda x: '19 SWS: {:.1f}%'.format(x))
	chart.add("20", data[20]/n*100, formatter=lambda x: '20 SWS: {:.1f}%'.format(x))
	try: 
		chart.add("21", data[21]/n*100, formatter=lambda x: '21 SWS: {:.1f}%'.format(x))
	except: 
		chart.add("21", 0, formatter=lambda x: '21 SWS: {:.1f}%'.format(x))
	try: 
		chart.add("22", data[22]/n*100, formatter=lambda x: '22 SWS: {:.1f}%'.format(x))
	except: 
		chart.add("22", 0, formatter=lambda x: '22 SWS: {:.1f}%'.format(x))
	chart.add("23", data[23]/n*100, formatter=lambda x: '23 SWS: {:.1f}%'.format(x))
	chart.add("24", data[24]/n*100, formatter=lambda x: '24 SWS: {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_sws-voll.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
