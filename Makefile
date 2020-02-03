.DEFAULT_GOAL := all

%:	prebuild
	@time -p $(MAKE) -j$(nproc) -s -f makefile.mk $@

prebuild:
	@python -B __init__.py

.PHONY: test
test:
	@python testing.py ${MODULE}

.INTERMEDIATE: prebuild