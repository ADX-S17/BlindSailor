OS := $(shell uname)

ifeq ($(OS),Linux)
	SHELL := /bin/bash
	GREP := /bin/grep
else
	SHELL := /bin/sh
	GREP := /usr/bin/grep
endif

PYTHON=$(shell command -v python)
PYTHON3=$(shell command -v python3)

tests:
	@set -e && cd tests && rm -f logs/* && for TEST in `/bin/ls [^_]*.py`; \
	do \
		echo "==== Starting test $$TEST ===="; \
		$(PYTHON3) $$TEST 0>&-;  \
		echo "==== End of test $$TEST ====\n"; echo "" ;\
	done && cd ..


itests:
	@set -e && cd tests && rm -f logs/* && for TEST in `/bin/ls [^_]*.py`; \
	do \
		echo "==== Starting test $$TEST ===="; \
		$(PYTHON3) $$TEST;  \
		echo "==== End of test $$TEST ====\n"; echo "" ;\
	done && cd ..

clean:
	#Clean .pyc and pycache
	find . -name "*.pyc" -type f | xargs rm
	find . -name "__pycache__" -type d | xargs rmdir

testclean:
	@cd tests && rm -f logs/* && rm -f config/* && cd ..

fclean: clean testclean
	rm -rf logs/*

.PHONY: tests clean install fclean testclean
.IGNORE:
.SILENT: clean fclean testclean
