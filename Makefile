SHELL := bash
LINE_LENGTH := 59
NO_COLOR := \e[39m
BLUE := \e[34m
GREEN := \e[32m

#----------------------------------------------------------

.PHONY: check
check : black-format flake8-lint success

.PHONY: unit-tests
unit-tests :
	@echo
	@echo -e '$(BLUE)unit-tests'
	@echo -e        '----------$(NO_COLOR)'
	@python3 -m unittest tests/test*.py -v

.PHONY: type-check
type-check :
	@echo
	@echo -e '$(BLUE)type-check'
	@echo -e 		'----------$(NO_COLOR)'
	@mypy formats

.PHONY: black-format
black-format :
	@echo
	@echo -e '$(BLUE)black-format'
	@echo -e 		'------------$(NO_COLOR)'
	@black formats -l $(LINE_LENGTH)

.PHONY: black-check
black-check :
	@echo
	@echo -e '$(BLUE)black-format'
	@echo -e 		'------------$(NO_COLOR)'
	@black formats -l $(LINE_LENGTH) --check

.PHONY: flake8-lint
flake8-lint :
	@echo
	@echo -e '$(BLUE)flake8-lint'
	@echo -e 		'-----------$(NO_COLOR)'
	@flake8 formats \
		--max-line-length $(LINE_LENGTH) \
		--ignore=E501,E731,F401 \
		--count \
		|| exit 1

.PHONY: success
success :
	@echo
	@echo -e '$(GREEN)ALL CHECKS COMPLETED SUCCESSFULLY$(NO_COLOR)'

#----------------------------------------------------------

.PHONY: set-hooks
set-hooks:
	@git config core.hooksPath .githooks
	@chmod +x .githooks/*