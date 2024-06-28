BUILD_DIR=build
PROB_IDS = $(notdir $(basename $(wildcard $(BUILD_DIR)/*.txt)))

noop=
space = $(noop) $(noop)
sep=,

all: build

build:
# generate solutions in build directory, the file names are problem numbers
	@mkdir -p $(BUILD_DIR)
	@echo "hello" > $(BUILD_DIR)/1.txt
	@echo "world" > $(BUILD_DIR)/2.txt

problems: $(BUILD_DIR)
	@echo "[$(subst $(space),$(sep),$(PROB_IDS))]" > $(PROBLEMS)

score: $(SCORES)
	@python3 .github/utils/score.py $(SCORES)

clean:
	@rm -rf $(BUILD_DIR)

PHONY: build