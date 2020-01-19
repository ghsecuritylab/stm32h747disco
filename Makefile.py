import os
from os.path import basename


def getProjectSettings():
    return {
        'PROJECT_NAME': basename(os.getcwd()),
        'FOLDER_OUT':   'Release/STM32F7xx/',
    }


def getCompilerSet():
    toolchain = '/opt/gcc-arm-none-eabi-8-2018-q4-major/'
    pfx = toolchain + 'bin/arm-none-eabi-'
    return {
        'CC':       pfx + 'gcc',
        'CXX':      pfx + 'g++',
        'LD':       pfx + 'gcc',
        'AR':       pfx + 'ar',
        'AS':       pfx + 'as',
        'OBJCOPY':  pfx + 'objcopy',
        'SIZE':     pfx + 'size',
        'OBJDUMP':  pfx + 'objdump',
        'INCLUDES': [
            toolchain + 'arm-none-eabi/include',
            toolchain + 'arm-none-eabi/include/c++/8.2.1',
            toolchain + 'arm-none-eabi/include/c++/8.2.1/arm-none-eabi',
            toolchain + 'arm-none-eabi/include/c++/8.2.1/backward',
            toolchain + 'lib/gcc/arm-none-eabi/8.2.1/include',
            toolchain + 'lib/gcc/arm-none-eabi/8.2.1/include-fixed'
        ]
    }


def getCompilerOpts():
    return {
        'MACROS': [
            '-DUSE_HAL_DRIVER',
            '-DSTM32H747xx',
            '-DUSE_STM32H747I_Discovery',
            '-DUSE_IOEXPANDER',
            '-DCORE_CM7',
        ],
        'MACHINE-OPTS': [
            '-mcpu=cortex-m7',
            '-mfpu=fpv5-d16',
            '-mfloat-abi=hard',
            '-mthumb'
        ],
        'OPTIMIZE-OPTS': [
            '-O0'
        ],
        'OPTIONS': [
            '-ffunction-sections',
            '-fstack-usage'
        ],
        'DEBUGGING-OPTS': [
            '-g3'
        ],
        'PREPROCESSOR-OPTS': [
            '-MP',
            '-MMD'
        ],
        'WARNINGS-OPTS': [
            '-Wall'
        ],
        'CONTROL-C-OPTS': [
            '-std=gnu11'
        ],
        'GENERAL-OPTS': [
            '--specs=nano.specs'
        ]
    }


def getLinkerOpts():
    return {
        'LINKER-SCRIPT': [
            '-TSTM32H747XIHx_FLASH_CM7_ETH.ld'
        ],
        'MACHINE-OPTS': [
            '-mcpu=cortex-m7',
            '-mfpu=fpv5-d16',
            '-mfloat-abi=hard',
            '-mthumb'
        ],
        'GENERAL-OPTS': [
            '--specs=nosys.specs'
        ],
        'LINKER-OPTS': [
            '-Wl,-Map=$(TARGET_MAP)',
            '-Wl,--gc-sections',
            '-static',
            '-Wl,--start-group',
            '-lc',
            '-lm',
            '-Wl,--end-group'
        ]
    }
