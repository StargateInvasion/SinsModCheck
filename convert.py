#The MIT License (MIT)
#Copyright (c) 2017 Stargate Invasion

import os
import glob
import sys
import hashlib
import subprocess
import errno
from shutil import copyfile


basegame = None
inputdir = None
output = None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def getType(filename):
    ext = os.path.splitext(filename)
    return ext[1].replace(".", "").lower()

def checkBin(inputpath, directory):
    # This was designed to convert the txt files to bin in an effort to identify ones that might have an issue
    # It creates a tmp bin file and then deletes it.  If it gets stuck or throws an error - investigate checked file.
    path = os.path.join(inputpath, directory)
    osname = os.name
    #print(glob.glob(os.path.join(path, '*')))
    for filename in glob.glob(os.path.join(path, '*')):
        gamefile = os.path.basename(filename)
        datatype = getType(gamefile)
        outfile = os.path.join(output, directory, gamefile)
        if not os.path.isdir(os.path.join(output, directory)):
            os.mkdir(os.path.join(output, directory))
        if datatype == "entity" or datatype == "brushes" or datatype == "mesh" or datatype == "particle":
            print "converting " + gamefile
            if osname == "posix":
                subprocess.call(['wine', os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, filename, outfile, 'txt'])
            else:
                subprocess.call([os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, filename, outfile, 'txt'])
        else:
            print "copying " + gamefile
            copyfile(filename, outfile)

if len(sys.argv) > 1:
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-o" and len(sys.argv) > i:
            output = sys.argv[i+1]
        elif sys.argv[i] == "-i" and len(sys.argv) > i:
            inputdir = sys.argv[i+1]
        i += 1
    if not basegame:
        if os.path.isdir("C:\Program Files (x86)\Steam\steamapps\common\Sins of a Solar Empire Rebellion"):
            basegame = "C:\Program Files (x86)\Steam\steamapps\common\Sins of a Solar Empire Rebellion"
        elif os.path.isdir("C:\Program Files\Steam\steamapps\common\Sins of a Solar Empire Rebellion"):
            basegame = "C:\Program Files\Steam\steamapps\common\Sins of a Solar Empire Rebellion"
        elif os.path.isdir(os.path.expanduser("~/.wine/drive_c/Program Files (x86)/Steam/steamapps/common/Sins of a Solar Empire Rebellion")):
            basegame = os.path.expanduser("~/.wine/drive_c/Program Files (x86)/Steam/steamapps/common/Sins of a Solar Empire Rebellion")    
    if not inputdir:
        inputdir = basegame
    
    if not os.path.isdir(os.path.expanduser(output)):
        mkdir_p(output)
        print "Creating dir: " + output
    
    print "Reading directory: " + inputdir
    for filename in glob.glob(os.path.join(inputdir, '*')):
        if os.path.isdir(filename):
            gamedir = os.path.basename(filename)
            checkBin(inputdir, gamedir)
        else:
            gamefile = os.path.basename(filename)
            print "copying " + gamefile
            outfile = os.path.join(output, gamefile)
            copyfile(filename, outfile)
else:
    print "Usage: convert.py -i <inputdirectory> -o <outputdirectory>"
    print "\tInput Directory will default to Sins basegame path if -i not specified"
    sys.exit()
