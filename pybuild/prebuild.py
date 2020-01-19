from pathlib import Path
import importlib.util
import inspect
import sys
import os
import time
import subprocess
import json


def printHeader(key: str, num: int):
    header = ''
    for _ in range(num):
        header += key
    return header


def listToString(l):
    aux = ""
    for item in l:
        aux += (str(item) + " ")
    aux.strip()
    return aux


def addToList(dstList: list, values):
    if isinstance(values, list):
        for item in values:
            dstList.append(item)
    elif isinstance(values, dict):
        for keys in values:
            for item in values[keys]:
                dstList.append(item)
    else:
        dstList.append(values)


def readModule(srcs: list, incs: list, flags: list, modPath, compilerOpts):
    lib = importlib.util.spec_from_file_location(str(modPath), str(modPath))
    mod = importlib.util.module_from_spec(lib)
    lib.loader.exec_module(mod)
    defList = []
    workspace = {
        'modPath': modPath.parent, 
        'compilerOpts': compilerOpts
        }
    result = getattr(mod, 'getSrcs')(workspace)
    addToList(srcs, result)
    result = getattr(mod, 'getIncs')(workspace)
    addToList(incs, result)
    try:
        result = getattr(mod, 'getCompilerOpts')(workspace)
        addToList(flags, result)
    except:
        pass


def read_Makefilepy():
    lib = importlib.util.spec_from_file_location('makefile', 'Makefile.py')
    mod = importlib.util.module_from_spec(lib)
    lib.loader.exec_module(mod)

    makevars = open('vars.mk', 'w')

    projSettings = None
    compSet = None
    compOpts = None

    try:
        projSettings = getattr(mod, 'getProjectSettings')()
        if projSettings['PROJECT_NAME']:
            makevars.write('PROJECT     = {}\n'.format(
                projSettings['PROJECT_NAME']))
        if projSettings['FOLDER_OUT']:
            projSettings['FOLDER_OUT'] = Path(projSettings['FOLDER_OUT'])
            makevars.write('PROJECT_OUT = {}\n'.format(
                projSettings['FOLDER_OUT']))
    except:
        pass

    makevars.write('\n')

    try:
        compSet = getattr(mod, 'getCompilerSet')()
        for sfx in ('CC', 'CXX', 'LD', 'AR', 'AS', 'OBJCOPY', 'SIZE', 'OBJDUMP'):
            if compSet[sfx]:
                makevars.write('{0:<10} := {1}\n'.format(sfx, compSet[sfx]))
    except:
        pass

    makevars.write('\n')

    try:
        compOpts = getattr(mod, 'getCompilerOpts')()
        if isinstance(compOpts, dict):
            for keys in compOpts:
                makevars.write('# {0}\n'.format(keys))
                makevars.write(
                    'COMPILER_FLAGS += {}\n'.format(listToString(compOpts[keys])))
        elif isinstance(compOpts, list):
            for item in compOpts:
                makevars.write('COMPILER_FLAGS += {}\n'.format(item))
    except:
        pass

    makevars.write('\n')

    try:
        linkOpts = getattr(mod, 'getLinkerOpts')()
        if isinstance(linkOpts, dict):
            for keys in linkOpts:
                makevars.write('# {0}\n'.format(keys))
                makevars.write('LDFLAGS += {}\n'.format(listToString(linkOpts[keys])))
        elif isinstance(linkOpts, list):
            for item in linkOpts:
                makevars.write('LDFLAGS += {}\n'.format(item))
    except:
        pass

    makevars.close()

    return projSettings, compOpts, compSet
# ------------------------------------------------------
# ------------------------------------------------------
# ------------------------------------------------------

modules = []

projSettings, compilerOpts, compilerSettings = read_Makefilepy()

# Load modules
for filename in Path('./').rglob('*[.|_]mk.py'):
    srcs = []
    flags = []
    incs = []
    print('Module: {}'.format(filename))
    readModule(srcs, incs, flags, filename, compilerOpts)
    modules.append([srcs, incs, flags, filename])

# Write CSRC
srcsfile = open('srcs.mk', 'w')

includes = []

for mod in modules:

    srcsfile.write("{}\n".format(printHeader('#', 52)))
    srcsfile.write("#{0:^50}#\n".format(str(mod[3])))
    srcsfile.write("{}\n".format(printHeader('#', 52)))

    for src in mod[0]:
        if str(src).endswith('.c'):
            srcsfile.write("CSRC += {}\n".format(src))
        elif str(src).endswith('.s'):
            srcsfile.write("ASSRC += {}\n".format(src))

    srcsfile.write('\n')

    for inc in mod[1]:
        srcsfile.write("INCS += -I{}\n".format(inc))
        includes.append(inc)

    srcsfile.write('\n')

    if mod[2]:
        for src in mod[0]:
            objs = str(src).replace('.c', '.o').replace('.s', '.o')
            srcsfile.write("{} : CFLAGS = {}\n".format(
                projSettings['FOLDER_OUT'] / str(objs), listToString(mod[2])))

    srcsfile.write('\n')

srcsfile.close()


# generate .vscode/c_cpp_properties.json

strIncs = []

if compilerSettings['INCLUDES']:
    includes += compilerSettings['INCLUDES']
    strIncs = [str(i) for i in includes]

defines = []
if compilerOpts['MACROS']:
    deflist = compilerOpts['MACROS']
    defines = [d.replace('-D', '') for d in deflist] 

c_cpp_properties = {
    "configurations": [
        {
            'name': 'ARM',
            'defines': defines,
            "compilerPath": "arm-none-eabi-gcc",
            "intelliSenseMode": "gcc-x64",
            "cStandard": "c11",
            "cppStandard": "c++17",
            "includePath": strIncs,
            "browse": {
                "path": strIncs,
                "limitSymbolsToIncludedHeaders": True,
                "databaseFilename": "${workspaceFolder}/.vscode/browse.vc.db"
            }
        }
    ],
    "version": 4
}

output = json.dumps(c_cpp_properties, indent=4)

if not os.path.exists('.vscode'):
    os.makedirs('.vscode')
fileout = open(".vscode/c_cpp_properties.json", "w")
fileout.write(output)
fileout.close()
