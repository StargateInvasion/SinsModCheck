import os
import glob
import sys

if len(sys.argv) > 3:
    if os.path.isfile(sys.argv[1]):
        filename = sys.argv[1]
        outfile = sys.argv[2]
        multiplier = float(sys.argv[3])
else:
    print("meshresize.py [input] [output] [multiplier]")
    sys.exit()

def fformat(ff):
    return '{:0.6f}'.format(ff).rstrip('0')+'0'[0:(ff%1==0)]

priorline = ""
file = open(outfile, "w")
for line in open(filename):
    if "Position" in line or "MaxBoundingExtents" in line or "MinBoundingExtents" in line:
        resize = []
        try:
            position1 = line.replace("]","").split("[")
            position2 = position1[1].strip()
            positions = position2.split(" ")
            for pos in positions:
                pos = float(pos.strip())
                if pos == 1.0 or pos == -1.0 or pos == 0.0:
                    resize.append(pos)
                else:
                    resize.append(pos * multiplier)
            reposition = position1[0] + "[ " + ' '.join(fformat(x) for x in resize)  + " ]"
            file.write(reposition + "\n")
        except Exception as e:
            print("Error in " + filename)
            print(e)
            print(line)
    elif "BoundingRadius" in line:
        try:
            position = line.split(" ")
            reposition = position[0] + " " + fformat(float(position[1].strip()) * multiplier)
            file.write(reposition + "\n")
        except Exception as e:
            print("Error in " + filename)
            print(e)
            print(line)
    else:
        file.write(line)
    priorline = line
file.close()
    

