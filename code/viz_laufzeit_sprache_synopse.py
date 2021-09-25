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
	data = data.loc[:,["include", "dauer_cat", "lang_frz", "lang_spa", "lang_ita", "lang_por"]]
	data = data[data["include"] == 1]
	#print(data.head())

	frz = data[data["lang_frz"] == 1]
	nfrz = frz.shape[0]
	frz = pd.Series(dict(Counter(frz["dauer_cat"])), name="frz")

	spa = data[data["lang_spa"] == 1]
	nspa = spa.shape[0]
	spa = pd.Series(dict(Counter(spa["dauer_cat"])), name="spa")

	ita = data[data["lang_ita"] == 1]
	nita = ita.shape[0]
	ita = pd.Series(dict(Counter(ita["dauer_cat"])), name="ita")

	por = data[data["lang_por"] == 1]
	npor = por.shape[0]
	por = pd.Series(dict(Counter(por["dauer_cat"])),name="por")

	data = pd.DataFrame([frz, spa, ita, por])
	data["sum"] = np.sum(data, axis=1)
	data = data.div(data["sum"], axis=0)*100
	data.drop("sum", axis=1, inplace=True)
	data.drop(["1-6", "~60", "66+", "other"], axis=1, inplace=True)
	data = data[["unb.", "~48", "~36", "~24", "~12"]]
	data = data.T
	data = data.fillna(0)
	print(data)
	return data


def viz(data): 
	dark_lighten_style = LightenStyle('#788207',
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
    	legend_at_bottom = False,
		legend_at_bottom_columns = 8,
		legend_box_size=32,
		range = (0,80))
	chart.title = "Vertragslaufzeiten nach Sprachen"
	chart.x_title = "Vertragslaufzeiten in Prozent"
	chart.y_title = "Monate"
	chart.x_labels = ["unb.", "~48", "~36", "~24", "~12"]
	chart.add("Französisch", data["frz"], formatter=lambda x: 'Frz.: {:.1f}%'.format(x))
	chart.add("Spanisch", data["spa"], formatter=lambda x: 'Spa: {:.1f}%'.format(x))
	chart.add("Italienisch.", data["ita"], formatter=lambda x: 'Ita.: {:.1f}%'.format(x))
	chart.add("Portugiesisch", data["por"], formatter=lambda x: 'Por.: {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_laufzeit-sprache-synopse.svg")


def main(): 
	data = get_data()
	data = prepare_data(data)
	viz(data)

main()	
