IMAGE_DIR ?= $(abspath ../../../assets/gen_files)

IMAGE_IDS = 0000 0025 0031 0044
IMAGES_ALGORITHM = $(foreach num,$(IMAGE_IDS),$(foreach type,EPnP iter,solvePnP$(type)_$(num).png))
IMAGES_LANDMARKS = $(foreach num,$(IMAGE_IDS),$(foreach type,5lm 5lmb iter,solvePnP$(type)_$(num).png))

TARGET_IMAGES = solvePnPcomparison landmarkscomparison

all: $(foreach im,$(TARGET_IMAGES),$(IMAGE_DIR)/$(im).png)

$(IMAGE_DIR)/solvePnPcomparison.png: $(IMAGES_ALGORITHM)
	montage $^ -tile 2x4 -mode Concatenate -geometry "+4+6" $@

$(IMAGE_DIR)/landmarkscomparison.png: $(IMAGES_LANDMARKS)
	montage $^ -quiet -crop 900x+188+0 +repage -tile 3x4 -mode Concatenate -geometry "+4+6" $@
