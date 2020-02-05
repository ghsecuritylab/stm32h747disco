from pybuild import MOD_PATH

def getSrcs(wk):
    return []

def getIncs(wk):
    return [MOD_PATH(wk) / 'LCDLog']