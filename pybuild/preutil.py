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


def getAllSrcs_C(wk):
    return getAllSrcs(wk, SrcType.C)


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


def getAllIncs_C(wk):
    return getAllIncs(wk, IncType.C)
