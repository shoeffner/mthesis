BUILD_DIR = build
SOURCE_DIR = src

FILES = $(addsuffix .md,$(addprefix $(SOURCE_DIR)/, eye_center_localization references))

PANDOC_COMMAND = pandoc --bibliography=bibliography.bib meta.yaml

thesis: $(FILES) | $(BUILD_DIR)
	$(PANDOC_COMMAND) \
	-o $(BUILD_DIR)/HoeffnerGaze.pdf \
	$(FILES)

.PRECIOUS: $(BUILD_DIR)/%.pdf

%: $(BUILD_DIR)/%.pdf ;

$(BUILD_DIR)/%.pdf: $(SOURCE_DIR)/%.md | $(BUILD_DIR)
	$(PANDOC_COMMAND) \
	-o $@ $<

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)
