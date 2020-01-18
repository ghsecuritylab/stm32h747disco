

def getSrcs(wk):
    return [
        'HttpServer/Src/app_ethernet.c',
        'HttpServer/Src/ethernetif.c',
        'HttpServer/Src/httpserver_netconn.c'
    ]


def getIncs(wk):
    return ['HttpServer/Src', 'HttpServer/Inc']
