all: build

build:
	@echo "implement me!"

score: $(SCORES)
	@python3 .github/utils/score.py $(SCORES)