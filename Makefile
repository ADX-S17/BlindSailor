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

all:
	@echo "make lt (=list tests)"
	@echo "make tests (=run all tests)"
	@echo "make tests T=app (=run app test only)"

lt:
	@ls -1 tests | grep test | cut -d '.' -f1 | cut -d '_' -f2,3,4 | sed -r '/^\s*$$/d'

test:
	@if [ ! -z ${T} ] ; then \
		$(eval ARGS := $(shell echo "-p '*${T}*'")) true; \
	fi
	@$(PYTHON3) -m unittest discover -v -s tests $(ARGS) 0>&-

itest:
	@if [ ! -z ${T} ] ; then \
		$(eval ARGS := $(shell echo "-p '*${T}*'")) true; \
	fi
	@$(PYTHON3) -m unittest discover -v -s tests $(ARGS)

ftest:
	@set -e && cd tests && rm -f logs/* && for TEST in `/bin/ls [^_]*.py`; \
	do \
		echo "==== Starting test $$TEST ===="; \
		$(PYTHON3) $$TEST 0>&- ; \
		if [ "$$?" == "1" ] ; then \
			echo ;\
			echo "**************************" ;\
			echo "**************************" ;\
			echo "********* FAILED *********" ;\
			echo "**************************" ;\
			echo "**************************" ;\
			echo ;\
			exit 1;\
		fi ;\
		echo "==== End of test $$TEST ====\n"; echo "" ;\
	done && cd ..


fitest:
	@set -e && cd tests && rm -f logs/* && for TEST in `/bin/ls [^_]*.py`; \
	do \
		echo "==== Starting test $$TEST ===="; \
		$(PYTHON3) $$TEST; \
		if [ "$$?" == "1" ] ; then \
			echo ;\
			echo "**************************" ;\
			echo "**************************" ;\
			echo "********* FAILED *********" ;\
			echo "**************************" ;\
			echo "**************************" ;\
			echo ;\
			exit 1;\
		fi ;\
		echo "==== End of test $$TEST ====\n"; echo "" ;\
	done && cd ..

testclean:
	@rm -f tests/logs/* && rm -rf tests/output/*
	@echo "Cleaned test files"

clean: testclean
	#Clean .pyc and pycache
	@find . -name "*.pyc" -type f | xargs -r rm
	@find . -name "__pycache__" -type d | xargs -r rmdir
	@echo "Cleaned python's compiled files"
	@rm -rf config

fclean: clean
	rm -rf logs/*

.PHONY: tests clean install fclean testclean
.IGNORE:
.SILENT: clean fclean testclean
