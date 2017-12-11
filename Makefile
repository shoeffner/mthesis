BUILD_DIR := build
SOURCE_DIR := src
OUTPUT_FORMAT ?= pdf
THESIS_FILE := HoeffnerGaze.$(OUTPUT_FORMAT)

META_FILES := meta.yaml
BIBLIOGRAPHY_FILE := bibliography.bib
CHAPTERS := $(shell cat chapters.list)
MD_FILES := $(addsuffix .md,$(addprefix $(SOURCE_DIR)/,$(CHAPTERS)))

PANFLUTE_FILTERS := $(addprefix bin/panflute/,$(shell ls bin/panflute))

BUILD_META_FILES := chapters.list Makefile
COMMON_DEPENDENCIES := $(BIBLIOGRAPHY_FILE) $(META_FILES) $(BUILD_META_FILES) $(PANFLUTE_FILTERS)

PANDOC_COMMAND := pandoc -s \
	--bibliography=$(BIBLIOGRAPHY_FILE) \
	--filter=panflute \
	$(META_FILES)

# Builds the complete thesis using the file list above.
$(BUILD_DIR)/$(THESIS_FILE): $(MD_FILES) $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) -o $@ $(MD_FILES)

# Allows to build `build/name.pdf` from `name`, where `name` is the name in
# `src/name.md`, thus it's not needed to provide the full target name.
.SECONDEXPANSION:
$(CHAPTERS): $(BUILD_DIR)/$$@.$(OUTPUT_FORMAT)

# Builds an individual pdf file from its corresponding markdown file.
$(BUILD_DIR)/%.$(OUTPUT_FORMAT): $(SOURCE_DIR)/%.md $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) -o $@ $< src/references.md

# Silently creates the build directory
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Silently cleans the build directory
clean:
	@rm -rf build
