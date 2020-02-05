from pybuild import preutil as p


def getSrcs(wk):
    return p.getAllSrcs_C(wk) 

    
def getIncs(wk):
    return p.getAllIncs_C(wk)
