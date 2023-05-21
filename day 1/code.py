import sys
import os
with open(os.path.join(sys.path[0], "data.txt"), "r") as f:
    max = 0
    cur = 0
    while(f.length() > 0):
        line = f.readline()
        if(line):
            cur += line
        else:
            if(max < cur):
                max = cur
                cur = 0
