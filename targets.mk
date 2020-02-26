TARGET     = Release/STM32F7xx/stm32h747disco.elf
TARGET_HEX = Release/STM32F7xx/stm32h747disco.hex
TARGET_BIN = Release/STM32F7xx/stm32h747disco.bin
TARGET_SIZE = Release/STM32F7xx/stm32h747disco.size
RESUME     = RESUME

TARGETS = $(RESUME)


$(TARGET): $(OBJECTS)
	$(call logger-compile,"OUT",$@)
	$(LD) -o $@ $(OBJECTS) $(LDFLAGS)

$(TARGET_HEX): $(TARGET)
	$(call logger-compile,"HEX",$@)
	$(OBJCOPY) -O ihex $(TARGET) Release/STM32F7xx/stm32h747disco.hex

$(TARGET_BIN): $(TARGET_HEX)
	$(call logger-compile,"BIN",$@)
	$(OBJCOPY) -O binary $(TARGET) Release/STM32F7xx/stm32h747disco.bin

$(TARGET_SIZE): $(TARGET_BIN)
	$(call logger-compile,"SIZE",$@)
	$(SIZE) -Ax $(TARGET) > Release/STM32F7xx/stm32h747disco.size

$(RESUME): $(TARGET_SIZE)
	$(call logger-compile,">>",$@)
	@python pybuild/armsize.py -F 1024000 -R 1054000 -s Release/STM32F7xx/stm32h747disco.size


clean_targets:
	rm -rf $(TARGET) $(TARGET_HEX) $(TARGET_BIN) $(TARGET_SIZE) $(RESUME)
