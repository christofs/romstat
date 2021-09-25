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
	data = data.loc[:,["include", "pos_lektorat", "pos_lfba", "pos_rat", "pos_wma", "sws_äqv"]]
	data = data[data["include"] == 1]
	data = data[data["sws_äqv"] != "N/A"]
	#print(data.head())

	lek = data[data["pos_lektorat"] == 1]
	nlkek = lek.shape[0]
	lek = pd.Series(dict(Counter(lek["sws_äqv"])), name="lek")

	lfba = data[data["pos_lfba"] == 1]
	nlfba = lfba.shape[0]
	lfba = pd.Series(dict(Counter(lfba["sws_äqv"])), name="lfba")

	rat = data[data["pos_rat"] == 1]
	nrat = rat.shape[0]
	rat = pd.Series(dict(Counter(rat["sws_äqv"])), name="rat")

	wma = data[data["pos_wma"] == 1]
	nwma = wma.shape[0]
	wma = pd.Series(dict(Counter(wma["sws_äqv"])),name="wma")

	data = pd.DataFrame([lek, lfba, rat, wma])
	data = data.drop(0.0, axis=1)
	data["sum"] = np.sum(data, axis=1)
	data = data.div(data["sum"], axis=0)*100
	data.drop("sum", axis=1, inplace=True)
	data = data.fillna(0)
	data = data.T
	data = data.drop(["10", "20", "6", "0", "2", "5", "7", "23", "24"])
	data = data.loc[["18", "16","14","12", "4"],:]
	print(data)
	return data


def viz(data): 
	dark_lighten_style = LightenStyle('#4c1d54',
		step=4, 
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
		range = (0,50))
	chart.title = "Lehrverpflichtung nach Stellentyp (Synopse)"
	chart.x_title = "Anteile der Lehrverpflichtungen in Prozent"
	chart.y_title = "SWS"
	chart.x_labels = ["18", "16", "14", "12", "4"]
	chart.add("Lekt.", data["lek"], formatter=lambda x: 'Lekt.: {:.0f}%'.format(x))
	chart.add("LfbA", data["lfba"], formatter=lambda x: 'LfbA: {:.0f}%'.format(x))
	chart.add("Ratst.", data["rat"], formatter=lambda x: 'Rat.: {:.0f}%'.format(x))
	chart.add("WMA", data["wma"], formatter=lambda x: 'WMA: {:.0f}%'.format(x))
	chart.render_to_file("../img/romanistik_lehrverpflichtung-stellentyp-synopse.svg")


def main(): 
	data = get_data()
	data = prepare_data(data)
	viz(data)

main()	
