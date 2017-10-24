BUILD_DIR := build
SOURCE_DIR := src
OUTPUT_FORMAT ?= pdf
THESIS_FILE := HoeffnerGaze.$(OUTPUT_FORMAT)

FILES := eye_center_localization references
OTHER_FILES := meta.yaml
FILE_LIST := $(addsuffix .md,$(addprefix $(SOURCE_DIR)/,$(FILES))) $(OTHER_FILES)
COMMON_DEPENDENCIES := bibliography.bib $(OTHER_FILES)

PANDOC_COMMAND := pandoc -s --bibliography=bibliography.bib meta.yaml

# Builds the complete thesis using the file list above.
$(BUILD_DIR)/$(THESIS_FILE): $(FILE_LIST) $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) -o $@ $(FILE_LIST)

# Allows to build `build/name.pdf` from `name`, where `name` is the name in
# `src/name.md`, thus it's not needed to provide the full target name.
.SECONDEXPANSION:
$(FILES): $(BUILD_DIR)/$$@.$(OUTPUT_FORMAT)

# Builds an individual pdf file from its corresponding markdown file.
$(BUILD_DIR)/%.$(OUTPUT_FORMAT): $(SOURCE_DIR)/%.md $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) -o $@ $<

# Creates the build directory silently
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

clean:
	@rm -rf build
