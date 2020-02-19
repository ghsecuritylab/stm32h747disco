from pathlib import Path, PosixPath


def getSrcs(wk):
    bsp = 'Drivers/BSP/STM32H747I-Discovery'
    bsp_srcs = list(Path(bsp).rglob('*.c'))

    hal = 'Drivers/STM32H7xx_HAL_Driver'
    hal_srcs = list(Path(hal).rglob('*.c'))

    no_hal_temp = list(Path(hal).rglob('*_template.c'))
    hal_srcs = list(set(hal_srcs) - set(no_hal_temp))

    no_hal_ll = list(Path(hal).rglob('stm32h7xx_ll_*'))
    hal_srcs = list(set(hal_srcs) - set(no_hal_ll))

    bsp_srcs.remove(PosixPath('Drivers/BSP/STM32H747I-Discovery/stm32h747i_discovery_ts.c'))
    bsp_srcs.remove(PosixPath('Drivers/BSP/STM32H747I-Discovery/stm32h747i_discovery_camera.c'))
    
    ll_srcs = [
        'Drivers/STM32H7xx_HAL_Driver/Src/stm32h7xx_ll_fmc.c',
        'Drivers/STM32H7xx_HAL_Driver/Src/stm32h7xx_ll_sdmmc.c',
        'Drivers/STM32H7xx_HAL_Driver/Src/stm32h7xx_ll_delayblock.c'
    ]
    
    
    comp_srcs = [
        'Drivers/BSP/Components/lan8742/lan8742.c',
        'Drivers/BSP/Components/otm8009a/otm8009a.c',
        'Drivers/BSP/Components/otm8009a/otm8009a_reg.c',
        'Drivers/BSP/Components/wm8994/wm8994.c',
        'Drivers/BSP/Components/wm8994/wm8994_reg.c',
        'Drivers/BSP/Components/is42s32800j/is42s32800j.c'
    ]
    return bsp_srcs + hal_srcs + comp_srcs + ll_srcs


def getIncs(wk):
    return [
        'Drivers/BSP/STM32H747I-Discovery',
        'Drivers/STM32H7xx_HAL_Driver/Inc',
        'Drivers/STM32H7xx_HAL_Driver/Inc/Legacy',
        'Drivers/CMSIS/Device/ST/STM32H7xx/Include',
        'Drivers/CMSIS/Include',
        'Drivers/BSP/Components/lan8742',
        'Drivers/BSP/Components/mt25tl01g',
        'Drivers/BSP/Components/otm8009a',
        'Drivers/BSP/Components/wm8994',
        'Drivers/BSP/Components/Common',
        'Drivers/BSP/Components/is42s32800j'
    ]
