import re


class Sym:
    def __init__(self, num: int, value: int, size: int, stype: str, bind: str, vis: str, ndx: str, name: str):
        self.num = num
        self.value = value
        self.size = size
        self.stype = stype
        self.bind = bind
        self.vis = vis
        self.ndx = ndx
        self.name = name


def getItemSym(line):
    match = re.findall('^[ ]+(?P<Num>[0-9]+):[ ]+(?P<Value>[a-fA-F0-9]+)[ ]+(?P<Size>[0-9]+)[ ]+(?P<Type>[a-zA-Z0-9]+)[ ]+(?P<Bind>[a-zA-Z0-9]+)[ ]+(?P<Vis>[a-zA-Z0-9]+)[ ]+(?P<Ndx>[a-zA-Z0-9]+)[ ]+(?P<Name>[a-zA-Z0-9_-]*).*', line)
    if match:
        s = Sym(
            int(match[0][0]),
            int(match[0][1], 16),
            int(match[0][2]),
            match[0][3],
            match[0][4],
            match[0][5],
            match[0][6],
            match[0][7]
        )
        return s
    else:
        return None


sizefile = open('simtable.txt')


ramUsage = 7

for line in sizefile:
    item = getItemSym(line)
    if item != None:
        if (item.value >= int("0x20000090", 16) and  item.value < int("0x2000ce14", 16)) and item.size > 0:
            ramUsage += item.size
            print('{}\t\t{}'.format(item.size, item.name))

print('{} B'.format(ramUsage))