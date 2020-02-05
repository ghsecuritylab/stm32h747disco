from pybuild import MOD_PATH


def getSrcs(wk):
    return [
        MOD_PATH(wk) / 'Src/app_ethernet.c',
        MOD_PATH(wk) / 'Src/ethernetif.c',
        MOD_PATH(wk) / 'Src/httpserver_netconn.c'
    ]


def getIncs(wk):
    return [ 
        MOD_PATH(wk) / 'Src',
        MOD_PATH(wk) / 'Inc'
    ]
