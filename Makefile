BUILD_DIR := build
SOURCE_DIR := src
OUTPUT_FORMAT ?= pdf
THESIS_FILE := HoeffnerGaze.$(OUTPUT_FORMAT)

ASSETS_DIR := assets
CHAPTERS_FILE := $(ASSETS_DIR)/chapters.list
CITATION_STYLE := $(ASSETS_DIR)/iet-computer-vision.csl
BIBLIOGRAPHY_FILE := $(ASSETS_DIR)/bibliography.bib

# Will be added as "content"
META_FILES := meta.yaml
CHAPTERS := $(shell cat $(CHAPTERS_FILE))
MD_FILES := $(addsuffix .md,$(addprefix $(SOURCE_DIR)/,$(CHAPTERS)))

PANFLUTE_FILTERS := $(addprefix bin/panflute/,$(shell ls bin/panflute))

BUILD_META_FILES := $(CHAPTERS_FILE) $(CITATION_STYLE) $(PANFLUTE_FILTERS) Makefile
COMMON_DEPENDENCIES := $(BIBLIOGRAPHY_FILE) $(META_FILES) $(BUILD_META_FILES)

PANDOC_COMMAND := pandoc -s \
	--bibliography=$(BIBLIOGRAPHY_FILE) \
	--filter=panflute \
	--csl=$(CITATION_STYLE) \
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
