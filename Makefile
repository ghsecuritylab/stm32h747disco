.DEFAULT_GOAL := all

%:	prebuild
	@time -p $(MAKE) -j$(nproc) -s -f makefile.mk $@

prebuild:
	@python -B pybuild/prebuild.py

.INTERMEDIATE: prebuild