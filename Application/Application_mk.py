from pybuild import preutil as p
from pybuild import MOD_PATH


def getSrcs(wk):
    return [
        MOD_PATH(wk) / 'App.c',
#         MOD_PATH(wk) / 'AudioPlayer.c',
        MOD_PATH(wk) / 'SDFatFs.c'
    ]

    
def getIncs(wk):
    return [MOD_PATH(wk)]
