BUILD_DIR := build
SOURCE_DIR := src
OUTPUT_FORMAT ?= pdf
THESIS_FILE := HoeffnerGaze

ASSETS_DIR := assets
CHAPTERS_FILE := $(ASSETS_DIR)/chapters.list
CITATION_STYLE := $(ASSETS_DIR)/international-journal-of-computer-vision.csl
BIBLIOGRAPHY_FILE := $(ASSETS_DIR)/bibliography.bib
GLOSSARY_FILE := $(ASSETS_DIR)/glossary.tex
TEMPLATE := thesis.latex

ENVIRONMENT := TEXINPUTS=$(ASSETS_DIR):

# Will be added as "content"
META_FILES := meta.yaml
CHAPTERS := $(shell cat $(CHAPTERS_FILE))
MD_FILES := $(addsuffix .md,$(addprefix $(SOURCE_DIR)/,$(CHAPTERS)))

PANFLUTE_FILTERS := $(addprefix bin/panflute/,$(shell ls bin/panflute))

BUILD_META_FILES := $(CHAPTERS_FILE) $(CITATION_STYLE) $(PANFLUTE_FILTERS) $(TEMPLATE) $(ASSETS_DIR)/thesistitlepage.sty Makefile
COMMON_DEPENDENCIES := $(BIBLIOGRAPHY_FILE) $(META_FILES) $(BUILD_META_FILES) $(GLOSSARY_FILE)

PANDOC_COMMAND := $(ENVIRONMENT) pandoc -s \
	--bibliography=$(BIBLIOGRAPHY_FILE) \
	--filter=panflute \
	--csl=$(CITATION_STYLE) \
	--template=$(TEMPLATE) \
	--highlight-style tango \
	--top-level-division=chapter \
	-V glossary=$(GLOSSARY_FILE) \
	$(META_FILES)

PANDOC_DRAFT_OPTIONS := -V draft:true
PANDOC_FINAL_OPTIONS := --toc -V lot:true -V loa:true -V loc:true -V lof:true -V appendix:true

# Builds the complete thesis using the file list above.
$(BUILD_DIR)/$(THESIS_FILE).pdf: $(BUILD_DIR)/$(THESIS_FILE).tex
	$(ENVIRONMENT) pdflatex $<
	$(ENVIRONMENT) pdflatex $< 1>/dev/null
	makeglossaries $(THESIS_FILE)
	$(ENVIRONMENT) pdflatex $< 1>/dev/null
	$(ENVIRONMENT) pdflatex $< 1>/dev/null
	makeglossaries $(THESIS_FILE)
	$(ENVIRONMENT) pdflatex $<
	mv $(THESIS_FILE).pdf $(BUILD_DIR)
	rm $(THESIS_FILE).*
	if [ -f texput.log ]; then rm texput.log ; fi

$(BUILD_DIR)/$(THESIS_FILE).tex: $(MD_FILES) $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) $(PANDOC_FINAL_OPTIONS) -o $@ $(MD_FILES)


# Allows to build `build/name.pdf` from `name`, where `name` is the name in
# `src/name.md`, thus it's not needed to provide the full target name.
.SECONDEXPANSION:
$(CHAPTERS): $(BUILD_DIR)/$$@.$(OUTPUT_FORMAT)

# Builds an individual pdf file from its corresponding markdown file.
$(BUILD_DIR)/%.$(OUTPUT_FORMAT): $(SOURCE_DIR)/%.md $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) $(PANDOC_DRAFT_OPTIONS) -o $@ $<

# Silently creates the build directory
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Silently cleans the build directory
clean:
	@rm -rf build
