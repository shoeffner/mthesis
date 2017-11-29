result.txt: tdfn_gui_summary.csv
	python extract_data.py palpfislength_r palpfislength_l > result.txt

tdfn_gui_summary.csv: download.py
	python download.py
