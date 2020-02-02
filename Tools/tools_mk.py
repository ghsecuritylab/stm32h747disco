from pybuild import preutil as p


def getSrcs(wk):
    return p.getAllSrcs(wk, p.SrcType.C)


def getIncs(wk):
    return p.getAllIncs(wk, p.IncType.C)
