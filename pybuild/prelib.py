from pathlib import Path
import importlib.util
from . import preconts as K


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
        K.MOD_WORKSPACE: modPath.parent,
        K.MOD_COMPILER_OPTS: compilerOpts
    }

    try:
        result = getattr(mod, K.MOD_F_GETSRCS)(workspace)
        addToList(srcs, result)
    except:
        pass

    try:
        result = getattr(mod, K.MOD_F_GETINCS)(workspace)
        addToList(incs, result)
    except:
        pass

    try:
        result = getattr(mod, K.MOD_F_GETCOMPILEROPTS)(workspace)
        flags.append(result)
    except:
        pass


def getLineSeparator(key: str, num: int):
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
                if (key == K.COMPOPTS_MACROS_KEY and isinstance(moduleCompileOps[key], dict)):
                    macros = macrosDictToString(moduleCompileOps[key])
                    mstr.append(macros)
                else:
                    mstr.append(listToString(moduleCompileOps[key]))
            
        elif isinstance(moduleCompileOps, list):
            for item in moduleCompileOps:
                mstr.append(item)
    
    return ' '.join(mstr) 


def read_Makefilepy():
    lib = importlib.util.spec_from_file_location(K.MAKEFILE_PY, K.MAKEFILE_PY)
    mod = importlib.util.module_from_spec(lib)
    lib.loader.exec_module(mod)

    makevars = open(K.VARS_MK, 'w')

    projSettings = None
    compSet = None
    compOpts = None

    try:
        projSettings = getattr(mod, K.MK_F_GETPROJECTSETTINGS)()
        if projSettings['PROJECT_NAME']:
            makevars.write('PROJECT     = {}\n'.format(
                projSettings['PROJECT_NAME']))
        if projSettings['FOLDER_OUT']:
            projSettings['FOLDER_OUT'] = Path(projSettings['FOLDER_OUT'])
            makevars.write('PROJECT_OUT = {}\n'.format(
                projSettings['FOLDER_OUT']))
    except Exception as e:
        print(e)

    makevars.write('\n')

    try:
        compSet = getattr(mod, K.MK_F_GETCOMPILERSET)()
        for sfx in (K.COMPILERSET_CC, K.COMPILERSET_CXX, K.COMPILERSET_LD, K.COMPILERSET_AR, K.COMPILERSET_AS, K.COMPILERSET_OBJCOPY, K.COMPILERSET_SIZE, K.COMPILERSET_OBJDUMP):
            if compSet[sfx]:
                makevars.write('{0:<10} := {1}\n'.format(sfx, compSet[sfx]))
    except:
        pass

    makevars.write('\n')

    try:
        compOpts = getattr(mod, K.MK_F_GETCOMPILEROPTS)()
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
        else:
            print("Not load getCompilerOpts")
    except:
        pass

    makevars.write('\n')

    try:
        linkOpts = getattr(mod, K.MK_F_GETLINKEROPTS)()
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
        targets = getattr(mod, K.MK_F_GETTARGETSSCRIPT)()
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

    except Exception as e:
        print(e)

    targetsmk.close()

    return projSettings, compOpts, compSet
