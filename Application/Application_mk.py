from preutil import *


def getSrcs(wk):
    return getAllSrcs(wk, SrcType.C)    

    
def getIncs(wk):
    return getAllIncs(wk, IncType.C)
