IMAGES = 68landmarks pupils3dmodel
EXTERNALS = pupil_detection_comparison solvePnPcomparison

IMAGE_DIR ?= $(abspath ../../assets/gen_files)
EXTERNAL_MAKE = IMAGE_DIR=$(IMAGE_DIR) $(MAKE) -C $(1)

all: $(foreach im,$(IMAGES),$(IMAGE_DIR)/$(im).png) $(EXTERNALS)

$(IMAGE_DIR)/68landmarks.png: dlibfacedetection.png figure_68_markup_sagonas2013.jpg | $(IMAGE_DIR)
	montage $^ -tile 2x -geometry "x1086>+5+0" $@

$(IMAGE_DIR)/pupils3dmodel.png: ./pose_0003.png ./pupils3d_0003.png | $(IMAGE_DIR)
	montage $^ -tile 2x1 -mode Concatenate -geometry "x700-50+0" $@

.PHONY: $(EXTERNALS)
$(EXTERNALS): | $(IMAGE_DIR)
	@$(call EXTERNAL_MAKE,$@)

clean:
	@rm -rf $(IMAGE_DIR)

$(IMAGE_DIR):
	@mkdir -p $(IMAGE_DIR)
