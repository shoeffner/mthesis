TARGET_DIR ?= $(abspath ../../assets/gen_files)

PUPIL_ACCURACIES = table-comptimes-pexels.md table-comptimes-BioID.md \
				   table-relative-errors-pexels.md table-relative-errors-BioID.md \
				   BioID_accuracy_vs_error.csv

FILES = $(PUPIL_ACCURACIES)

all: $(foreach f,$(FILES),$(TARGET_DIR)/$(f))

$(foreach f,$(PUPIL_ACCURACIES),$(TARGET_DIR)%$(f)): pupil_accuracies.py BioID.csv pexels.csv Makefile
	python ./pupil_accuracies.py

BioID.csv: dataacquisition/build/bioid
	$(shell cd dataacquisition/build && ./bioid > ../../BioID.csv)

pexels.csv: dataacquisition/build/pexels
	$(shell cd dataacquisition/build && ./pexels > ../../pexels.csv)

dataacquisition/build/%: | dataacquisition/build
	cd dataacquisition/build && make $*

dataacquisition/build:
	@mkdir -p dataacquisition/build
	@cd dataacquisition/build && cmake ..
