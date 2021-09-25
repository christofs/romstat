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
	data = data.loc[:,["include", "pos_lektorat", "pos_lfba", "pos_rat", "pos_wma", "dauer_cat"]]
	data = data[data["include"] == 1]
	#print(data.head())

	lek = data[data["pos_lektorat"] == 1]
	nlkek = lek.shape[0]
	lek = pd.Series(dict(Counter(lek["dauer_cat"])), name="lek")

	lfba = data[data["pos_lfba"] == 1]
	nlfba = lfba.shape[0]
	lfba = pd.Series(dict(Counter(lfba["dauer_cat"])), name="lfba")

	rat = data[data["pos_rat"] == 1]
	nrat = rat.shape[0]
	rat = pd.Series(dict(Counter(rat["dauer_cat"])), name="rat")

	wma = data[data["pos_wma"] == 1]
	nwma = wma.shape[0]
	wma = pd.Series(dict(Counter(wma["dauer_cat"])),name="wma")

	data = pd.DataFrame([lek, lfba, rat, wma])
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
	dark_lighten_style = LightenStyle('#004466',
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
	chart.title = "Vertragslaufzeiten nach Stellentyp"
	chart.x_title = "Vertragslaufzeiten in Prozent"
	chart.y_title = "Monate"
	chart.x_labels = ["unb.", "~48", "~36", "~24", "~12"]
	chart.add("Lekt.", data["lek"], formatter=lambda x: 'Lekt.: {:.0f}%'.format(x))
	chart.add("LfbA", data["lfba"], formatter=lambda x: 'LfbA: {:.0f}%'.format(x))
	chart.add("Ratst.", data["rat"], formatter=lambda x: 'Rat.: {:.0f}%'.format(x))
	chart.add("WMA", data["wma"], formatter=lambda x: 'WMA: {:.0f}%'.format(x))
	chart.render_to_file("../img/romanistik_laufzeit-stellentyp-synopse.svg")


def main(): 
	data = get_data()
	data = prepare_data(data)
	viz(data)

main()	
