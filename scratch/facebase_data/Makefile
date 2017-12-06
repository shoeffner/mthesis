METRICS = incanthwidth outcanthwidth palpfislength_r palpfislength_l labfiswidth

result.txt: tdfn_gui_summary.csv extract_data.py Makefile
	python extract_data.py $(METRICS) > result.txt

tdfn_gui_summary.csv: download.py
	python download.py
