import re
from os.path import join
import glob
import os
import pandas as pd
import pygal
from collections import Counter
from pygal.style import LightenStyle
import numpy as np


def get_data(): 
	with open("../data/romanistik-stellen_datensatz_2014-2021.csv", "r", encoding="utf8") as infile: 
		data = pd.read_csv(infile, sep="\t")
		#print(data.head())
		return data


def prepare_data(data): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", "domain_lit", "domain_ling", "domain_mkw", "domain_fdid", "domain_other", "dauer_cat", "domain_count"]]
	data = data[data["include"] == 1]
	data = data[data["domain_count"] > 0]
	#print(data.head())
	#print("Anzahl der Datenpunkte", n)
	from collections import Counter

	lit = data[data["domain_lit"] == 1]
	nlit = lit.shape[0]
	lit = pd.Series(dict(Counter(lit["dauer_cat"])), name="lit")

	ling = data[data["domain_ling"] == 1]
	nling = ling.shape[0]
	ling = pd.Series(dict(Counter(ling["dauer_cat"])), name="ling")

	fdid = data[data["domain_fdid"] == 1]
	nfdid = fdid.shape[0]
	fdid = pd.Series(dict(Counter(fdid["dauer_cat"])), name="fdid")

	mkw = data[data["domain_mkw"] == 1]
	nmkw = mkw.shape[0]
	mkw = pd.Series(dict(Counter(mkw["dauer_cat"])),name="mkw")

	data = pd.DataFrame([lit, ling, fdid, mkw])
	data["sum"] = np.sum(data, axis=1)
	print(data)
	data = data.div(data["sum"], axis=0)*100
	data.drop("sum", axis=1, inplace=True)
	data = data[["unb.", "~48", "~36", "~24", "~12"]]
	data = data.T
	print(data)
	return data


def viz(data): 
	dark_lighten_style = LightenStyle('#700925',
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
		legend_box_size=32,
		range = (0,50))
	chart.title = "Vertragslaufzeiten nach Fachgebieten"
	chart.x_title = "Vertragslaufzeiten in Prozent"
	chart.y_title = "Monate"
	chart.x_labels = ["unb.", "~48", "~36", "~24", "~12"]
	chart.add("Literaturwiss.", data["lit"], formatter=lambda x: 'Lit.: {:.1f}%'.format(x))
	chart.add("Linguistik.", data["ling"], formatter=lambda x: 'Ling.: {:.1f}%'.format(x))
	chart.add("Medien- und Kulturwiss.", data["mkw"], formatter=lambda x: 'MKW: {:.1f}%'.format(x))
	chart.add("Fachdidaktik", data["fdid"], formatter=lambda x: 'Fachd.: {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_laufzeit-fachgebiete-synopse.svg")


def main(): 
	data = get_data()
	data = prepare_data(data)
	viz(data)

main()	
