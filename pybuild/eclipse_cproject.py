# Generate .cproject from .cproject_template
#
# Wildcards:
#   <!--wildcard_c_includes-->      : C Includes
#   <!--wildcard_c_symbols-->       : C Symbols
#   <!--wildcard_cpp_includes-->    : C++ Includes
#   <!--wildcard_cpp_symbols-->     : C++ Symbols

# listconf = {'C_INCLUDES': [...], 'C_SYMBOLS' : [...], 'CPP_INCLUDES': [...], 'CPP_SYMBOLS': [...]}
from pathlib import Path

CPROJECT_TEMPLATE = '.cproject_template'
CPROJECT = '.cproject'

WILDCARD_C_INCLUDES = '<!--wildcard_c_includes-->'
WILDCARD_C_SYMBOLS = '<!--wildcard_c_symbols-->'


def generate_cproject(listconf: dict):

    try:
        cproject_template = open(CPROJECT_TEMPLATE, 'r')
        cproject = open(CPROJECT, 'w')

        for line in cproject_template:
            if(line.strip() == WILDCARD_C_INCLUDES):
                if listconf['C_INCLUDES']:
                    cproject.write((writeXmlIncludes(listconf['C_INCLUDES'])))
            if(line.strip() == WILDCARD_C_SYMBOLS):
                if listconf['C_SYMBOLS']:
                    cproject.write((writeXmlSymbols(listconf['C_SYMBOLS'])))
            else:
                cproject.write(line)

    except IOError:
        print('Files .cproject or .cproject_template no accessible')
    finally:
        cproject_template.close()
        cproject.close()


def writeXmlIncludes(incList):
    directory = Path("./srcs.mk")
    directory = str(directory.absolute().parent.name)
    w = []
    for i in incList:
        if str(i).startswith('/'):  # absolute path
            w.append("<listOptionValue builtIn=\"false\" value=\"" +
                     str(i) + "\"/>\n")
        else:  # realative path
            w.append(
                "<listOptionValue builtIn=\"false\" value=\"&quot;${workspace_loc:/"+directory+"/"+str(i)+"}&quot;\"/>\n")

    return ''.join(w)


def writeXmlSymbols(symList):
    w = []
    for sym in symList:
        sym = str(sym).replace("\\\"", "&quot;")
        w.append("<listOptionValue builtIn=\"false\" value=\""+sym+"\"/>\n")

    return ''.join(w)
