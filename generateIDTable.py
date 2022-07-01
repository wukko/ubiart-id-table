#
# https://github.com/wukko/ubiart-id-table
#
# UbiArt idtable.idt file generator from existing IPK bundles by https://github.com/wukko
# Tested on PC version of Just Dance 2017.
# This script should work for other UbiArt games that also use IDTable for file list verification, such as Just Dance 2015 - 2022 on PS4 (orbis).
#
# UbiArt CRC32 implementation by https://github.com/InvoxiPlayGames (https://gist.github.com/InvoxiPlayGames/4320e6781fa8d17baedd22f6e6ff779c).
#
# This script includes all matching files in current directory and its subdirectories when used standalone. Keep this in mind when using it.
#
# Credit is required when this script is used in other project to both me (https://github.com/wukko) and https://github.com/InvoxiPlayGames.

import os
import math

# Modify these variables for standalone use if needed
out = "idtable.idt"
bext = ".ipk"
gfext = ".gf"
ignore = ["patch"]
p = ["pc", "durango", "scarlett", "orbis", "prospero", "ggp"]

def shifter(a, b, c):
    d = 0
    a = (a - b - c) ^ (c >> 0xd)
    a = a & 0xffffffff
    b = (b - a - c) ^ (a << 0x8)
    b = b & 0xffffffff
    c = (c - a - b) ^ (b >> 0xd)
    c = c & 0xffffffff
    a = (a - c - b) ^ (c >> 0xc)
    a = a & 0xffffffff
    d = (b - a - c) ^ (a << 0x10)
    d = d & 0xffffffff
    c = (c - a - d) ^ (d >> 0x5)
    c = c & 0xffffffff
    a = (a - c - d) ^ (c >> 0x3)
    a = a & 0xffffffff
    b = (d - a - c) ^ (a << 0xa)
    b = b & 0xffffffff
    c = (c - a - b) ^ (b >> 0xf)
    c = c & 0xffffffff
    return a, b, c

def crc(data):
    i = 0
    a = 0x9E3779B9
    b = 0x9E3779B9
    c = 0
    length = len(data)
    
    if length > 0xc:
        while i < math.floor(length / 0xc):
            a += (((((data[i * 0xc + 0x3] << 8) + data[i * 0xc + 0x2]) << 8) + data[i * 0xc + 0x1]) << 8) + data[i * 0xc];
            b += (((((data[i * 0xc + 0x7] << 8) + data[i * 0xc + 0x6]) << 8) + data[i * 0xc + 0x5]) << 8) + data[i * 0xc + 0x4];
            c += (((((data[i * 0xc + 0xb] << 8) + data[i * 0xc + 0xa]) << 8) + data[i * 0xc + 0x9]) << 8) + data[i * 0xc + 0x8];
            i += 1
            a, b, c = shifter(a, b, c)
    
    c += length;
    i = length - (length % 0xc);
    
    decide = (length % 0xc) - 1
    if decide >= 0xa: c += data[i + 0xa] << 0x18;
    if decide >= 0x9: c += data[i + 0x9] << 0x10;
    if decide >= 0x8: c += data[i + 0x8] << 0x8;
    if decide >= 0x7: b += data[i + 0x7] << 0x18;
    if decide >= 0x6: b += data[i + 0x6] << 0x10;
    if decide >= 0x5: b += data[i + 0x5] << 0x8;
    if decide >= 0x4: b += data[i + 0x4];
    if decide >= 0x3: a += data[i + 0x3] << 0x18;
    if decide >= 0x2: a += data[i + 0x2] << 0x10;
    if decide >= 0x1: a += data[i + 0x1] << 0x8;
    if decide >= 0x0: a += data[i + 0x0];
    
    a, b, c = shifter(a, b, c)
    
    return c

def nameOnly(name, ext):
    name = name.split('/')[len(name.split('/'))-1]
    for i in p:
        name = name.replace(ext, '').replace('_'+i, '')
    return name

def generateIDTable(cwd, out, bext, gfext, ignore):
    bl = []
    bn = 0

    for root, dir_names, file_names in os.walk(cwd):
        for f in file_names:
            path = os.path.join(root, f).replace(cwd, '')[1:]
            if path[-4:] == bext or path[-3:] == gfext:
                bl.append(path.replace('\\', '/'))

    bl = [b for b in bl if not nameOnly(b, bext) in ignore]

    with open(out, "wb") as f:
        f.write((len(bl) + 1).to_bytes(4, "big")) # hash counter offset might be wrong, but that's what official idtable usually has (+1)
        for i in bl:
            f.write(crc(bytearray(i.upper(), "utf8")).to_bytes(4, "big"))
            f.write(bn.to_bytes(4, "big"))
            bn += 1

if __name__ == "__main__":
    generateIDTable(os.getcwd(), out, bext, gfext, ignore)
