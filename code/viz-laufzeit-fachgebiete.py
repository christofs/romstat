import re
from os.path import join
import glob
import os
import pandas as pd
import pygal
from collections import Counter
from pygal.style import LightenStyle


domains = ["domain_lit", "domain_ling", "domain_mkw", "domain_fdid", "domain_other"]
plotnames = ["litw", "sprachw", "mkw", "fdid", "andere"]
titles = ["Literaturwiss.", 
		"Sprachwiss.",
		"Medien- und Kulturwiss.",
		"Fachdidaktik",
		"weitere Bereiche"]
params = {"domains": domains, "plotnames":plotnames, "titles":titles}


def get_data(): 
	with open("../data/romanistik-stellen_datensatz_2014-2021.csv", "r", encoding="utf8") as infile: 
		data = pd.read_csv(infile, sep="\t")
		#print(data.head())
		return data


def prepare_data(data, params, i): 
	# Filter down to useable data
	data = data.fillna(0)
	data = data.loc[:,["include", params["domains"][i], "dauer_cat", "domain_count"]]
	data = data[data["include"] == 1]
	data = data[data["domain_count"] > 0]
	data = data[data[params["domains"][i]] == 1]
	#print(data.head())
	n = data.shape[0]
	print("Anzahl der Datenpunkte", n)
	from collections import Counter
	data = dict(Counter(data["dauer_cat"]))
	print(data)
	return data,n


def viz(data,n, params, i): 
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
		legend_box_size=32,
		range = (0,50))
	chart.title = "Vertragslaufzeiten (nur " + params["titles"][i] + ")"
	chart.x_title = "Anteile der Vertragslaufzeiten in Prozent (n="+str(n)+")"
	try: 
		chart.add("1-6", data["1-6"]/n*100, formatter=lambda x: '1-6 M.: {:.1f}%'.format(x))
	except: 
		chart.add("1-6", 0, formatter=lambda x: '1-6 M.: {:.1f}%'.format(x))		
	try: 
		chart.add("~12", data["~12"]/n*100, formatter=lambda x: '~12 M.: {:.1f}%'.format(x))
	except: 
		chart.add("~12", 0, formatter=lambda x: '~12 M.: {:.1f}%'.format(x))	
	chart.add("~24", data["~24"]/n*100, formatter=lambda x: '~24 M.: {:.1f}%'.format(x))
	chart.add("~36", data["~36"]/n*100, formatter=lambda x: '~36 M.: {:.1f}%'.format(x))
	chart.add("~48", data["~48"]/n*100, formatter=lambda x: '~48 M.: {:.1f}%'.format(x))
	chart.add("~60", data["~60"]/n*100, formatter=lambda x: '~60 M.: {:.1f}%'.format(x))
	chart.add("66+", data["66+"]/n*100, formatter=lambda x: '66+ M.: {:.1f}%'.format(x))
	chart.add("unb.", data["unb."]/n*100, formatter=lambda x: 'unbefristet {:.1f}%'.format(x))
	chart.render_to_file("../img/romanistik_laufzeit-fachgebiete-" + params["plotnames"][i] +".svg")
			
			


def main(params): 
	for i in range(0, 5):
		data = get_data()
		data,n = prepare_data(data, params, i)
		viz(data,n, params, i)
	

main(params)	
