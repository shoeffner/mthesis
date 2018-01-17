IMAGE_DIR ?= $(abspath ../../../assets/gen_figures)

IMAGES = $(foreach num,0000 0025 0031 0044,$(foreach type,EPnP iter,solvePnP$(type)_$(num).png))

$(IMAGE_DIR)/solvePnPcomparison.png: $(IMAGES)
	montage $^ -tile 2x4 -mode Concatenate -geometry "+4+6" $@

