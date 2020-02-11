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

install:
	@./resources/scripts/install_dep.sh && ./resources/scripts/install_sihd.sh && ./resources/scripts/make_links.sh

sihd:
	@./resources/scripts/install_sihd.sh && ./resources/scripts/make_links.sh


links:
	@./resources/scripts/make_links.sh

uninstall:
	@./resources/scripts/uninstall.sh

lt:
	@ls -1 tests | grep test | cut -d '.' -f1 | cut -d '_' -f2 | sed -r '/^\s*$$/d'

tests:
	@if [ ! -z ${T} ] ; then \
		$(eval ARGS := $(shell echo "-p '*${T}*'")) true; \
	fi
	@$(PYTHON3) -m unittest discover -v -s tests $(ARGS) 0>&-

itests:
	@if [ ! -z ${T} ] ; then \
		$(eval ARGS := $(shell echo "-p '*${T}*'")) true; \
	fi
	@$(PYTHON3) -m unittest discover -v -s tests $(ARGS)

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
