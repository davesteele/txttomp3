#!/usr/bin/python3

import re
import sys
from collections import defaultdict

def line_gen(txt):
    chapter = 1
    longestline = 0

    for line in txt.split('\n'):
        longestline = max([longestline, len(line)])

        match = re.search("Chapter ([0-9]+)", line)
        if match:
            chapter = int(match.group(1))
        yield (chapter, line)

    print("longest line is", longestline)

chapters = defaultdict(lambda: [])


infile = sys.argv[1]

for chapnum, line in line_gen(open(infile, 'r').read()):
    print(chapnum, line)
    chapters[chapnum].append(line)

for chap in chapters:
    name = f"chapter{chap:03}.txt"
    with open(name, 'w') as fp:
        for line in chapters[chap]:
            fp.write(line)
            fp.write("\n")


