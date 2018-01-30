BUILD_DIR := build
SOURCE_DIR := src
OUTPUT_FORMAT ?= pdf
THESIS_FILE := HoeffnerGaze

ASSETS_DIR := assets
CHAPTERS_FILE := $(ASSETS_DIR)/chapters.list
CITATION_STYLE := $(ASSETS_DIR)/springer-socpsych-author-date.mod.csl
BIBLIOGRAPHY_FILE := $(ASSETS_DIR)/bibliography.bib
GLOSSARY_FILE := $(ASSETS_DIR)/glossary.tex
TEMPLATE := thesis.latex

ENVIRONMENT := TEXINPUTS=$(ASSETS_DIR):

# Will be added as "content"
META_FILES := meta.yaml
CHAPTERS := $(shell cat $(CHAPTERS_FILE))
MD_FILES := $(addsuffix .md,$(addprefix $(SOURCE_DIR)/,$(CHAPTERS)))
SOURCE_FILES := $(addprefix $(SOURCE_DIR)/,$(shell ls $(SOURCE_DIR)))
ASSETS_FILES := $(shell find assets -type f | grep -v "/build/" | grep -v "/\." | grep -v ".bak$$")

PANFLUTE_FILTERS := $(addprefix bin/panflute/,$(shell ls bin/panflute))

BUILD_META_FILES := $(CHAPTERS_FILE) $(CITATION_STYLE) $(PANFLUTE_FILTERS) $(TEMPLATE) $(ASSETS_FILES) Makefile
COMMON_DEPENDENCIES := $(BIBLIOGRAPHY_FILE) $(META_FILES) $(BUILD_META_FILES) $(GLOSSARY_FILE)

PANDOC_COMMAND := $(ENVIRONMENT) pandoc -s \
	--filter=pandoc-fignos \
	--filter=panflute \
	--bibliography=$(BIBLIOGRAPHY_FILE) \
	--csl=$(CITATION_STYLE) \
	--template=$(TEMPLATE) \
	--highlight-style tango \
	--top-level-division=chapter \
	-V glossary=$(GLOSSARY_FILE) \
	$(META_FILES)

PRINT_INFO = @echo "Pagecount Color (Total): `gs -o - -sDEVICE=inkcov $(1) | grep CMYK | grep -v '0.00000  0.00000  0.00000' | wc -l | tr -d ' '` (`pdfinfo $(1) | grep Pages: | rev | cut -d" " -f1 | rev`)"

PANDOC_DRAFT_OPTIONS := -V draft:true
PANDOC_FINAL_OPTIONS := --toc -V lot:true -V loa:true -V loc:true -V lof:true -V appendix:true

PDFLATEX = $(ENVIRONMENT) pdflatex $(1)

# To tee undefined references
SHELL := /bin/bash
UNDEF_FILE := build/undef_refs

# Builds the complete thesis using the file list above.
$(BUILD_DIR)/$(THESIS_FILE).pdf: $(BUILD_DIR)/$(THESIS_FILE).tex
	@# Postprocessing: Convert captions without short captions but with ;; in their captions to short captions.
	python ./bin/shortcaps.py $<
	$(call PDFLATEX,$<)
	$(call PDFLATEX,$<) 1>/dev/null
	makeglossaries $(THESIS_FILE)
	$(call PDFLATEX,$<) 1>/dev/null
	$(call PDFLATEX,$<) 1>/dev/null
	makeglossaries $(THESIS_FILE)
	# Store undefined references
	$(call PDFLATEX,$<) | tee >(grep "LaTeX Warning: Reference" | sed "s/.*\`\(.*\)\'.*/\1/" >> $(UNDEF_FILE))
	@# move resulting pdf to build directory to keep working directory clean
	@mv $(THESIS_FILE).pdf $(BUILD_DIR)
	@# cleanup intermediate files
	@rm $(THESIS_FILE).*
	@if [ -f texput.log ]; then rm texput.log ; fi
	$(call PRINT_INFO,$@)
	@# Search for undefined references and print the results
	@for i in $$(cat $(UNDEF_FILE)); do ack $$i src ; done
	@# Print TODOs
	@ack "TODO|todo" src

$(BUILD_DIR)/$(THESIS_FILE).tex: $(SOURCE_FILES) $(COMMON_DEPENDENCIES) figures evaluation | $(BUILD_DIR)
	$(PANDOC_COMMAND) $(PANDOC_FINAL_OPTIONS) -o $@ $(MD_FILES) 2>&1 | tee >(grep "pandoc-citeproc" | cut -d' ' -f3 > $(UNDEF_FILE))

.PHONY: figures
figures:
	@$(MAKE) -C ./scratch/figures
	@$(MAKE) -C ./scratch/BioIDImages all

.PHONY: evaluation
evaluation:
	@$(MAKE) -C ./scratch/evaluation

# Allows to build `build/name.pdf` from `name`, where `name` is the name in
# `src/name.md`, thus it's not needed to provide the full target name.
.SECONDEXPANSION:
$(basename $(notdir $(SOURCE_FILES))): $(BUILD_DIR)/$$@.$(OUTPUT_FORMAT)

# Builds an individual pdf file from its corresponding input file.
.SECONDEXPANSION:
$(BUILD_DIR)/%.$(OUTPUT_FORMAT): $$(shell ls $(SOURCE_DIR)/%.*) $(COMMON_DEPENDENCIES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) $(PANDOC_DRAFT_OPTIONS) -o $@ $<

# Silently creates the build directory
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Silently cleans the build directory and latex intermediate files from the
# working directory.
clean:
	@rm -rf build
	@rm $(THESIS_FILE).*
