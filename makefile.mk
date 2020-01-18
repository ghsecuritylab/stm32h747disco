## Local functions
define logger-compile
	@printf "%6s\t%-30s\n" $(1) $(2)
endef

.DEFAULT_GOAL := all

CSRC  =
ASSRC = 
INCS  = 
COMPILER_FLAGS =
LDFLAGS =


include vars.mk
include srcs.mk


OBJECTS = $(CSRC:%.c=$(PROJECT_OUT)/%.o) $(ASSRC:%.s=$(PROJECT_OUT)/%.o)

TARGET     = $(PROJECT_OUT)/$(PROJECT).elf
TARGET_BIN = $(PROJECT_OUT)/$(PROJECT).bin
TARGET_HEX = $(PROJECT_OUT)/$(PROJECT).hex
TARGET_MAP = $(PROJECT_OUT)/$(PROJECT).map


%.o : CFLAGS = $(COMPILER_FLAGS)


$(PROJECT_OUT)/%.o: %.c
	$(call logger-compile,"CC",$<)
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $<


$(PROJECT_OUT)/%.o: %.s
	$(call logger-compile,"AS",$<)
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $<


$(TARGET): $(OBJECTS) $(LDSCRIPT)
	$(call logger-compile,"LD",$@)
	$(LD) -o $@ $(OBJECTS) $(LDFLAGS)
	$(OBJCOPY) -O ihex $@ $(TARGET_HEX)
	$(SIZE) -Ax $@ > size.txt
	@python pybuild/armsize.py -F 1024000 -R 128000 -s size.txt
	@rm size.txt


all: $(TARGET)


clean:
	@echo 'CLEAN'
	rm -rf $(PROJECT_OUT)

.PHONY: clean