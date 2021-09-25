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
	data = data.loc[:,["include", "domain_lit", "domain_spr", "domain_ling", "domain_mkw", "domain_fdid", "domain_other"]]
	data = data[data["include"] == 1]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = {"domain_lit":sum(data["domain_lit"]),
			"domain_ling":sum(data["domain_ling"]),
			"domain_mkw":sum(data["domain_mkw"]),
			"domain_fdid":sum(data["domain_fdid"]),
			"domain_spr":sum(data["domain_spr"]),
			"domain_other":sum(data["domain_other"]),
			}
	print(data)
	return data,n


def viz(data,n): 
	dark_lighten_style = LightenStyle('#8f0a94',
		step=8, 
		font_family="FreeSans",
		label_font_size = 12,
		major_label_font_size = 12,
		value_label_font_size = 12,
		value_font_size = 14,
		title_font_size = 16)
	chart = pygal.HorizontalBar(
		style=dark_lighten_style,
		print_values = True,
		show_legend = False,
    	legend_at_bottom = False,
		legend_at_bottom_columns = 8,
		legend_box_size=32)
	chart.title = "Ausschreibungen nach Fachgebieten"
	chart.x_title = "Anteile der Fachgebiete in Prozent (Mehrfachnennungen möglich; n="+str(n)+")"
	chart.add("domain_lit", data["domain_lit"]/n*100, formatter=lambda x: 'Literaturwiss.: {:.1f}%'.format(x))
	chart.add("domain_ling", data["domain_ling"]/n*100, formatter=lambda x: 'Sprachwiss.: {:.1f}%'.format(x))
	chart.add("domain_mkw", data["domain_mkw"]/n*100, formatter=lambda x: 'Medien- und Kulturwiss.: {:.1f}%'.format(x))
	chart.add("domain_spr", data["domain_spr"]/n*100, formatter=lambda x: 'Sprachpraxis {:.1f}%'.format(x))
	chart.add("domain_fdid", data["domain_fdid"]/n*100, formatter=lambda x: 'Fachdidaktik {:.1f}%'.format(x))
	chart.add("domain_other", data["domain_other"]/n*100, formatter=lambda x: 'Weitere Bereiche {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_alle-fachgebiete.svg")
			
			


def main(): 
	data = get_data()
	data,n = prepare_data(data)
	viz(data,n)
	

main()	
