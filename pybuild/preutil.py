from pathlib import Path


class SrcType:
    C = ['.c']
    CPP = ['.C', '.cc', '.cpp', '.CPP', '.c++', '.cp', '.cxx']
    ASM = ['.s', '.S', '.asm']

    
class IncType:
    C = ['.h']
    CPP = ['.h', '.hpp', '.h++', '.hh']


def getAllSrcs(wk, srcType: SrcType):
    srcs = []
    for ext in srcType:
        srcs += list(Path(wk['modPath']).rglob('*' + ext))
    return srcs


def getSrcsByRgx(wk, *regexs):
    srcs = []
    for r in regexs:
        srcs += list(Path(wk['modPath']).rglob(r))
        
    srcs = list(dict.fromkeys(srcs))
    return srcs


def getAllIncs(wk, incType: IncType):
    incsfiles = []
    for ext in incType:
        incsfiles += list(Path(wk['modPath']).rglob('*' + ext))
    
    incs = []
    for i in incsfiles:
        incs.append(i.parent)
        
    incs = list(dict.fromkeys(incs))
    return incs
