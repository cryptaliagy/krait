.PHONY: test
test :
	pytest

.PHONY: check
check :
	mypy

.PHONY: lint
lint :
	flake8
