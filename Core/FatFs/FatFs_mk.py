from pybuild import preutil as p


def getSrcs(wk):
    return ['Core/FatFs/Src/sd_diskio_dma.c']

    
def getIncs(wk):
    return ['Core/FatFs/Inc']  