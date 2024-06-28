BUILD_DIR=build
PROB_IDS = $(notdir $(basename $(wildcard $(BUILD_DIR)/*.txt)))

noop=
space = $(noop) $(noop)
sep=,$(space)

all: build

build:
# put solutions in build directory and the file names are problem numbers
	@mkdir -p $(BUILD_DIR)
	@echo "hello" > $(BUILD_DIR)/1.txt
	@echo "world" > $(BUILD_DIR)/2.txt

problems: $(BUILD_DIR)
	@echo "[$(subst $(space),$(sep),$(PROB_IDS))]" > $(PROBLEMS)

score: $(SCORES)
	@python3 .github/utils/score.py $(SCORES)

clean:
	@rm -rf $(BUILD_DIR)

PHONY: build problems score clean