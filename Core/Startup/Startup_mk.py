from pybuild import MOD_PATH


def getSrcs(wk):
    return [
        MOD_PATH(wk) / 'startup_stm32h747xx.s',
        MOD_PATH(wk) / 'syscalls.c'
    ]


def getIncs(wk):
    return []
