import re
import sys
import getopt


class ItemSizeStat:
    def __init__(self, name, size, addr):
        self.name = name
        self.size = size
        self.addr = addr

    def string(self):
        return self.name + " " + self.size + " " + self.addr

    def getAddr(self):
        return self.addr

    def getSize(self):
        return self.size


def getSizeAddr(line):
    x = re.search("^([A-Za-z0-9_\.]+)[ ]+([a-z0-9]+)[ ]+([a-z0-9]+).*", line)
    if(x):
        return ItemSizeStat(x.group(1), x.group(2), x.group(3))
    else:
        None


def printKB(value, decimals=1):
    return ('{:.'+str(decimals)+'f}').format(value/1000)

def printPrtg(value, decimals=1):
    return ('{:.'+str(decimals)+'f}').format(value*100)


def main(argv):
    totalFlashLen = 0
    totalRAMLen = 0
    sizefile = ''

    try:
        opts, args = getopt.getopt(
            argv, "hF:R:s:", ["flash-len=", "ram-len=", "size-file="])
    except getopt.GetoptError:
        print('armsize.py -F <flash-len:int> -R <ram-len:int> -s <size-file:file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-F', '--flash-len'):
            totalFlashLen = int(arg)
        elif opt in ('-R', '--ram-len'):
            totalRAMLen = int(arg)
        elif opt in ('-s', '--size-file'):
            sizefile = arg

    file = open(sizefile, "r")

    STATE_FIND = 0
    STATE_READ = 1
    STATE_END = 2

    state = STATE_FIND

    itemsSize = []

    for line in file:
        if(state == STATE_FIND):
            x = re.search("^section[ ]+size[ ]+addr.*", line)
            if(x):
                state = STATE_READ
        elif state == STATE_READ:
            x = re.search("^Total.*", line)
            if(x):
                state = STATE_END
            else:
                item = getSizeAddr(line)
                itemsSize.append(item)

    RAM_ADDR = int("0x20000000", 16)
    FLASH_ADDR = int("0x8000000", 16)
    TOTAL_RAM = float(totalRAMLen)
    TOTAL_FLASH = float(totalFlashLen)
    RAM_USAGE = 0
    FLASH_USAGE = 0

    for item in itemsSize:
        itemAddr = int(item.getAddr(), 16)
        if(itemAddr >= RAM_ADDR):
            RAM_USAGE = RAM_USAGE + int(item.getSize(), 16)
        elif(itemAddr >= FLASH_ADDR and itemAddr < RAM_ADDR):
            FLASH_USAGE = FLASH_USAGE + int(item.getSize(), 16)

    print('{:<6}{:>14}{:>14}{:>14}'.format('REGION', 'SIZE', 'USED', 'USAGE (%)'))

    perc = (float(RAM_USAGE) / TOTAL_RAM)
    print("RAM:   {:>10} KB {:>10} KB {:>10} %".format(
        printKB(TOTAL_RAM), printKB(RAM_USAGE), printPrtg(perc)))

    perc = (float(FLASH_USAGE) / TOTAL_FLASH)
    print("FLASH: {:>10} KB {:>10} KB {:>10} %".format(
        printKB(TOTAL_FLASH), printKB(FLASH_USAGE), printPrtg(perc)))


if __name__ == "__main__":
    main(sys.argv[1:])
