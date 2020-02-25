# Copyright (c) 2020, Ericson Joseph
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of pyMakeTool nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from pathlib import Path
import importlib.util
import inspect
import sys
import os
import time
import subprocess
import json
import re
from . import eclipse_cproject as cp
from builtins import dict

USE_EXCLUDE_FOLDERS = True


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

def macrosDictToString(macros):
    mstr = []
    if isinstance(macros, dict):
        for key in macros:
            if macros[key] != None and macros[key] != '':
                if isinstance(macros[key], str):
                    mstr.append('-D{}=\\\"{}\\\"'.format(key, macros[key]))
                elif isinstance(macros[key], bool):
                    mstr.append('-D{}={}'.format(key, '1' if macros[key] else '0'))
                else:
                    mstr.append('-D{}={}'.format(key, macros[key]))
            else:
                mstr.append('-D{}'.format(key))
    
    return ' '.join(mstr)

def compilerOptsByModuleToLine(compOpts):
    mstr = []
    for moduleCompileOps in compOpts:
        if isinstance(moduleCompileOps, dict):
            for key in moduleCompileOps:
                if (key == 'MACROS' and isinstance(moduleCompileOps[key], dict)):
                    macros = macrosDictToString(moduleCompileOps[key])
                    mstr.append(macros)
                else:
                    mstr.append(listToString(moduleCompileOps[key]))
            
        elif isinstance(moduleCompileOps, list):
            for item in moduleCompileOps:
                mstr.append(item)
    
    return ' '.join(mstr)            

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
        flags.append(result)
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
            for key in compOpts:
                makevars.write('# {0}\n'.format(key))
                if (key == 'MACROS' and isinstance(compOpts[key], dict)):
                    makevars.write('COMPILER_FLAGS += {}\n'.format(macrosDictToString(compOpts[key])))
                else:
                    makevars.write('COMPILER_FLAGS += {}\n'.format(listToString(compOpts[key])))
        
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
                makevars.write(
                    'LDFLAGS += {}\n'.format(listToString(linkOpts[keys])))
        elif isinstance(linkOpts, list):
            for item in linkOpts:
                makevars.write('LDFLAGS += {}\n'.format(item))
    except:
        pass

    makevars.close()

    targetsmk = open('targets.mk', 'w')

    try:
        targets = getattr(mod, 'getTargetsScript')()
        if isinstance(targets, dict):
            if len(targets) == 0:
                pass
            else:
                labels = []
                targetval = []
                targetsct = []
                logkeys = []
                for k in targets:
                    labels.append(k)
                    targetval.append(targets[k]['FILE'])
                    targetsct.append(targets[k]['SCRIPT'])
                    if 'LOGKEY' in targets[k]:
                        logkeys.append(targets[k]['LOGKEY'])
                    else:
                        logkeys.append('>>')

                for i in range(len(targetval)):
                    targetsmk.write("{0:<10} = {1}\n".format(labels[i], targetval[i]))

                targetsmk.write('\nTARGETS = $({})\n\n'.format(labels[len(targetval)-1]))

                for i in range(len(labels)):
                    if labels[i] == 'TARGET':
                        targetsmk.write("\n$({}): {}\n".format(labels[i],'$(OBJECTS)'))
                    else:
                        targetsmk.write("\n$({}): $({})\n".format(labels[i],labels[i-1]))
                    
                    targetsmk.write('\t$(call logger-compile,"{}",$@)\n'.format(logkeys[i]))
                    script = targetsct[i]
                    script = ' '.join(script)
                    targetsmk.write('\t{}\n'.format(script))

                targetsmk.write('\n')

                targetsmk.write("\n{}:\n".format('clean_targets'))
                targetlist = ('$('+l+')' for l in labels)
                targetsmk.write('\trm -rf {}\n'.format(' '.join(targetlist)))

                # keytargetlist = list(targets.keys())
                # keytarget = keytargetlist[0]
                # targetsmk.write("{} = {}\n".format('TARGET', keytarget))
                # targetsmk.write('\n\n')
                # targetsmk.write("{}: {}\n".format('$(TARGET)','$(OBJECTS)'))
                # targetsmk.write('\t{}\n'.format('$(call logger-compile,"LD",$@)'))
                # script = targets[keytarget]
                # script = ' '.join(script)
                # targetsmk.write('\t{}\n'.format(script))
                # targetsmk.write('\n\n')
                # targetsmk.write('{} = {}'.format('TARGETS', '$(TARGET)'))

                # for idx in range(1, len(keytargetlist)):



    except:
        pass

    targetsmk.close()

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
                projSettings['FOLDER_OUT'] / str(objs), compilerOptsByModuleToLine(mod[2])))

    srcsfile.write('\n')

srcsfile.close()


# generate .vscode/c_cpp_properties.json

strIncs = []
aux = []

if compilerSettings['INCLUDES']:
    aux += compilerSettings['INCLUDES']
if includes:
    aux += includes

strIncs = [str(i) for i in aux]

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

# generate .cproject from .cproject_template

# cproject_template = open('.cproject_template', 'r')
# cproject = open('.cproject', 'w')

# directory = Path("./srcs.mk")
# directory = str(directory.absolute().parent.name)

# for line in cproject_template:
#     if(line.strip().startswith("<wildcard_project_include/>")):

#         if compilerSettings['INCLUDES']:
#             for compIncs in compilerSettings['INCLUDES']:
#                 cproject.write("<listOptionValue builtIn=\"false\" value=\""+ str(compIncs) + "\"/>\n")

#         for incs in includes:
#             cproject.write("<listOptionValue builtIn=\"false\" value=\"&quot;${workspace_loc:/"+directory+"/"+str(incs)+"}&quot;\"/>\n")

#     else:
#         cproject.write(line)

# print("-------------------------------------------------")
# print("All folders")
# Exclude folders

listToExclude = []

if (USE_EXCLUDE_FOLDERS):
    allIncFoldes = []
    includes = [str(i) for i in includes]

    for filename in Path('.').rglob('*.h'):
        allIncFoldes.append(str(filename.parent))

    allIncFoldes = list(dict.fromkeys(allIncFoldes))

    allIncFoldes.sort()

#     print(allIncFoldes)

    filtedist = []
    parent = ""
    for p in allIncFoldes:
        if parent == "":
            parent = p
            filtedist.append(p)
        elif(p.startswith(parent+"/")):
            None
        else:
            parent = p
            filtedist.append(p)

    allIncFoldes = filtedist

#     for a in allIncFoldes:
#         print(a)


    # print("-------------------------------------------------")
    # print("Build Includes")
    # for inc in includes:
    #     print(inc)

    # print("-------------------------------------------------")
    # print("Filter")
    p = re.compile('^(I|i)nc(lude)*$')

    for allinc in allIncFoldes:
        aux = allinc + '/'
        if not any(aux.startswith(a + "/") for a in includes):
            if not str(allinc).startswith('Test/ceedling') and not allinc == '.':
                auxpath = Path(allinc)
                if p.match(auxpath.name):
                    listToExclude.append(str(auxpath.parent))
                else:
                    listToExclude.append(allinc)
            
    listToExclude.append('Test/ceedling')
    
    
    
#     for r in listToExclude:
#         mvpath = Path(r)
#         if (mvpath.name.startswith("_")):
#             continue
#         
#         if Path('Test') in mvpath.parents:
#             continue
# 
#         if str(mvpath) == '.' or str(mvpath) == '..':
#             continue
# 
#         dstpath = str(mvpath.parent / str("_"+mvpath.name))
#         print("mv {} {}".format(mvpath, dstpath))
#         try:
#             os.rename(mvpath, dstpath)
#         except:
#             None

#     print(listToExclude)

#     listToInclude = []
# 
#     for inc in includes:
#         nameInc = Path(inc).name
#         pathExclude = str(Path(inc).parent / str("_"+nameInc))
#         if pathExclude in allIncFoldes:
#             listToInclude.append(pathExclude)
# 
#     # print("TO INCLUDE --------------------------------------")
# 
#     for t in listToInclude:
#         mvpath = Path(t)
#         if str(mvpath.name).startswith("_"):
#             dstname = str(mvpath.name)[1:]
#             dstpath = str(mvpath).replace(mvpath.name, dstname)
#             print("mv {} {}".format(mvpath, dstpath))
#             try:
#                 os.rename(mvpath, dstpath)
#             except:
#                 None

cproject_setting = {
    'C_INCLUDES': strIncs,
    'C_SYMBOLS': compilerOpts['MACROS'],
    'C_EXCLUDE': listToExclude
}

cp.generate_cproject(cproject_setting)


