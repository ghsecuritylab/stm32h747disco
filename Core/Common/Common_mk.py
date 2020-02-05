from pybuild import MOD_PATH


def getSrcs(wk):
    return [MOD_PATH(wk) / 'Src/system_stm32h7xx_eth.c']


def getIncs(wk):
    return []
