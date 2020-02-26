# generate .vscode/c_cpp_properties.json
import os
import json

# No implement yet
compilerOpts = {}
compilerSettings = {}
includes = []

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