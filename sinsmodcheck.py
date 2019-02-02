#The MIT License (MIT)
#Copyright (c) 2017 Stargate Invasion

import os
import glob
import sys
import hashlib
import subprocess

basegameplaintext = "~/Documents/workspace/SinsRef/Rebellion"

version = '1.16'
verbose = False
graph = False
skipbin = False
fullbin = False
buildman = False
showcost = False
excludebase = False

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def baseDup(directory):
    basepath = os.path.join(basegame, directory)
    path = os.path.join(rootpath, directory)
    osname = os.name
    for filename in glob.glob(os.path.join(path, '*')):
        gamefile = os.path.basename(filename)
        if os.path.exists(os.path.join(basepath, gamefile)):
            filemd5 = md5(filename)
            sinsmd5 = md5(os.path.join(basepath, gamefile))
            if filemd5 == sinsmd5:
                print "\tUnnecessary File: " + gamefile
                #os.remove(filename)
            elif not skipbin and directory != 'Texture' and directory != 'Sound':
                fline = open(filename, "r").readline().rstrip().encode("hex").replace("efbbbf", "").decode("hex") #Remove Byte Order Mark
                bline = open(os.path.join(basepath, gamefile), "r").readline().rstrip()
                if fline == 'TXT' and bline == 'BIN':
                    datatype = getType(gamefile)
                    if datatype == "entity" or datatype == "brushes" or datatype == "mesh" or datatype == "particle":
                        print "checking " + gamefile
                        if osname == "posix":
                            subprocess.call(['wine', os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, filename, filename + ".tmp", 'bin'])
                        else:
                            subprocess.call([os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, filename, filename + ".tmp", 'bin'])
                        filemd5 = md5(filename + ".tmp")
                        os.remove(filename + ".tmp")
                        if filemd5 == sinsmd5:
                            print "\tUnnecessary File: " + gamefile
                            #os.remove(filename)
                        else:
                            pass
                            #subprocess.call(['wine', os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, os.path.join(basepath, gamefile), filename + ".base", 'txt'])

def checkBin(directory):
    # This was designed to convert the txt files to bin in an effort to identify ones that might have an issue
    # It creates a tmp bin file and then deletes it.  If it gets stuck or throws an error - investigate checked file.
    path = os.path.join(rootpath, directory)
    osname = os.name
    for filename in glob.glob(os.path.join(path, '*')):
        gamefile = os.path.basename(filename)
        datatype = getType(gamefile)
        if datatype == "entity" or datatype == "brushes" or datatype == "mesh" or datatype == "particle":
            print "checking " + gamefile
            if osname == "posix":
                subprocess.call(['wine', os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, filename, filename + ".tmp", 'bin'])
            else:
                subprocess.call([os.path.join(basegame, 'ConvertData_Rebellion.exe'), datatype, filename, filename + ".tmp", 'bin'])
            filemd5 = md5(filename + ".tmp")
            os.remove(filename + ".tmp")
        
def getType(filename):
    ext = os.path.splitext(filename)
    return ext[1].replace(".", "")

if len(sys.argv) > 1:
    rootpath = sys.argv[1]
    if not os.path.isdir(os.path.expanduser(rootpath)):
        print "\tUsage: simsmodcheck.py <moddirectory> --showunused --graphexport"
        print "\nThe Mod directory '" + rootpath + " was not found."
        sys.exit()
else:
    print "\tUsage: simsmodcheck.py <moddirectory> --showunused --graphexport --skipbin --fullbin --manifest"
    sys.exit()

if len(sys.argv) > 2:
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i].replace("-", "")
        if arg == "showunused" or arg == "v" or arg == "verbose":
            verbose = True
        elif arg == "graphexport":
            graph = True
        elif arg == "skipbin":
            skipbin = True
        elif arg == "fullbin":
            fullbin = True
        elif arg == "manifest":
            buildman = True
        elif arg == "showcost":
            showcost = True
        elif arg == "excludebase":
            excludebase = True
        i += 1

basegame = None
if os.path.isdir("C:\Program Files (x86)\Steam\steamapps\common\Sins of a Solar Empire Rebellion"):
    basegame = "C:\Program Files (x86)\Steam\steamapps\common\Sins of a Solar Empire Rebellion"
elif os.path.isdir("C:\Program Files\Steam\steamapps\common\Sins of a Solar Empire Rebellion"):
    basegame = "C:\Program Files\Steam\steamapps\common\Sins of a Solar Empire Rebellion"
elif os.path.isdir(os.path.expanduser("~/.wine/drive_c/Program Files (x86)/Steam/steamapps/common/Sins of a Solar Empire Rebellion")):
    basegame = os.path.expanduser("~/.wine/drive_c/Program Files (x86)/Steam/steamapps/common/Sins of a Solar Empire Rebellion")


print "\n***** Sins of Solar Empire Mod File Verifcation " + version + " *****"
if not basegame:
    print "\nThe Sins of a Solar Empire Rebellion base game was not found.  The script may identify items that are missing in the mod that could default to the base game.  Modify the script to include your basegame path.\n"
if verbose:
    print "\nNote: Not all dependencies have been identified and Binary files in the mod are not read.  Files listed as UNUSED may be referenced by these binary files or not yet identified.\n"

if fullbin:
    print '\n*** Full File Check (Create Bin as conversion check) ***'
    print '\tNote: this process will create a temporary file and then delete it'
    checkBin('Mesh')
    checkBin('GameInfo')
    checkBin('Particle')
    checkBin('Window')
    sys.exit()

texturelist = []
soundlist = []
brushlist = []
meshlist = []
stringlist = []
meshfiles = []
entitymanifest = []
entitylist = []
entitylinked = []
particlefiles = []
particlelist = []
binfiles = []
basegamemeshes = []
basegametextures = []
basegameparticles = []
basegameentites = []
basegamesounds = []
soundlinks = []
soundfilelinks = []
modentities = []
squadentities = []

path = os.path.join(rootpath, 'GameInfo')
for filename in glob.glob(os.path.join(path, '*.entity')):
    entityfilename = os.path.basename(filename)
    modentities.append(entityfilename.lower())

def isModEntity(file):
    global modentities
    return file.lower() in modentities
    
def notInMod(entity, file):
    if entity != "BuffWormHoleTeleport":
        print "Entity not in Mod: " + entity + " via " + file

def readFile(filename):
    if not os.path.isfile(filename):
        print "\tCouldn't find " + filename
        return
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    global asurantime
    global asurancost
    global humantime
    global humancost
    global goauldtime
    global goauldcost
    entityfilename = os.path.basename(filename)
    entitylist.append(entityfilename)
    linecount = 0
    researchsubject = False
    researchpos = None
    costcomplete = False
    totaltime = 0
    totalcost = 0
    maxlevels = 0
    playercount = 0
    playercountentity = 0
    #print entityfilename
    entityType = ""
    with open(filename, 'r+') as f:
        for line in f:
            if linecount == 0 and line.startswith("BIN"):
                binfiles.append(entityfilename)
                break
            linecount += 1
            if entityfilename.startswith("Player") and line.strip().startswith("count "):
                if playercountentity > 0 and playercount > 0 and playercountentity != playercount:
                    print "\t Found a count of " + str(playercount) + " but the entityDefName below it has a count of " + str(playercountentity) + " in " + entityfilename
                playercount = int(line.split()[1])
                playercountentity = 0
            
            if 'entityType "' in line:
                entityType = line.replace('entityType', "").replace('"', "").strip()
            if isModEntity(entityType + ".entity"):
                #print "Entity Match: " + entityType + " via " + filename
                entitylinked.append([entityType, filename])
            elif os.path.isfile(os.path.join(plaintextpath, entityType + ".entity")):
                notInMod(entityType, filename)
                readFile(os.path.join(plaintextpath, entityType + ".entity"))
            if entityType == "ResourceAsteroid":
                entitylinked.append([entityfilename.replace(".entity", ""), filename])
            elif entityType == "PipCloud":
                entitylinked.append([entityfilename.replace(".entity", ""), filename])
            if 'entityType "ResearchSubject"' in line and 'ARTIFACT' not in filename:
                researchsubject = True
            elif "environmentMapName " in line:
                brushfilename = line.replace('environmentMapName', "").replace('"', "").strip()
                if brushfilename != "" and not [brushfilename, filename] in texturelist:
                    texturelist.append([brushfilename, filename])
            elif "environmentIlluminationMapName " in line:
                brushfilename = line.replace('environmentIlluminationMapName', "").replace('"', "").strip()
                if brushfilename != "" and not [brushfilename, filename] in texturelist:
                    texturelist.append([brushfilename, filename])
            elif "beamGlowTextureName " in line:
                brushfilename = line.replace('beamGlowTextureName', "").replace('"', "").strip()
                if brushfilename != "" and not brushfilename in texturelist:
                    texturelist.append([brushfilename, filename])
            elif "beamCoreTextureName " in line:
                brushfilename = line.replace('beamCoreTextureName', "").replace('"', "").strip()
                if brushfilename != "" and not [brushfilename, filename] in texturelist:
                    texturelist.append([brushfilename, filename])
            elif "textureName " in line:
                brushfilename = line.replace('textureName', "").replace('"', "").strip()
                if brushfilename != "" and not [brushfilename, filename] in texturelist:
                    texturelist.append([brushfilename, filename])
            elif 'title ' in line:
                stringname = line.replace('title', "").replace('"', "").strip()
                if stringname != "" and not [stringname, filename] in stringlist:
                    stringlist.append([stringname, filename])
            elif 'nameStringID ' in line:
                stringname = line.replace('nameStringID', "").replace('"', "").strip()
                if stringname != "" and not [stringname, filename] in stringlist:
                    stringlist.append([stringname, filename])
            elif 'descStringID ' in line:
                stringname = line.replace('descStringID', "").replace('"', "").strip()
                if stringname != "" and not [stringname, filename] in stringlist:
                    stringlist.append([stringname, filename])
            elif 'toggleStateOnNameStringID ' in line:
                stringname = line.replace('toggleStateOnNameStringID', "").replace('"', "").strip()
                if stringname != "" and not [stringname, filename] in stringlist:
                    stringlist.append([stringname, filename])
            elif 'toggleStateOnDescStringID ' in line:
                stringname = line.replace('toggleStateOnDescStringID', "").replace('"', "").strip()
                if stringname != "" and not [stringname, filename] in stringlist:
                    stringlist.append([stringname, filename])
            elif 'counterDescriptionStringID' in line:
                stringname = line.replace('counterDescriptionStringID', "").replace('"', "").strip()
                if stringname != "" and not [stringname, filename] in stringlist:
                    stringlist.append([stringname, filename])
            elif 'EffectName' in line:
                particlename = line.strip().split()[1].replace('"', "").strip()
                if particlename != "" and not [particlename, filename] in particlelist:
                    particlelist.append([particlename, filename])
            elif 'meshNameIncreasedEffectName' in line or 'meshNameDecreasedEffectName' in line:
                particlename = line.strip().split()[1].replace('"', "").strip()
                if particlename != "" and not [particlename, filename] in particlelist:
                    particlelist.append([particlename, filename])
            elif 'planetImpactEffectName' in line:
                particlename = line.strip().split()[1].replace('"', "").strip()
                if particlename != "" and not [particlename, filename] in particlelist:
                    particlelist.append([particlename, filename])
            elif 'ExhaustParticleSystemName' in line:
                particlename = line.strip().split()[1].replace('"', "").strip()
                if particlename != "" and not [particlename, filename] in particlelist:
                    particlelist.append([particlename, filename])
            elif 'entityDefName ' in line:
                playercountentity += 1
                entityname = line.replace('entityDefName', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'ruinPlanetType' in line:
                entityname = line.replace('ruinPlanetType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'spaceMineType ' in line:
                entityname = line.replace('spaceMineType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'bonus "' in line and entityType == "Planet":
                entityname = line.replace('bonus ', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'cannonShellType ' in line:
                entityname = line.replace('cannonShellType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'buffType ' in line:
                entityname = line.replace('buffType', "").replace('"', "").strip()
                if entityname != "" and entityname != "BuffWormHoleTeleport" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'frigateType ' in line:
                entityname = line.replace('frigateType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'buffToApplyOnImpact ' in line:
                entityname = line.replace('buffToApplyOnImpact', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'fighterEntityDef ' in line:
                entityname = line.replace('fighterEntityDef', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'postSpawnBuff ' in line:
                entityname = line.replace('postSpawnBuff', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'type "' in line and (entityType == "Ability" or entityType == "Buff"):
                entityname = line.replace('type', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'ability:' in line:
                entityname = line.strip().split()[1].replace('"', "")
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'squadTypeEntityDef:' in line:
                entityname = line.strip().split()[1].replace('"', "")
                if entityname != "" and not filename in squadentities:
                    squadentities.append(filename)
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif "CommandPoints" in line:
                if "baseCommandPoints" not in line and "maxNumCommandPoints" not in line:
                    line = f.next()
                value = line.strip().split()[1].replace('"', "")
                if float(value) > 0 and not filename in squadentities and entityType != "Cosmetic":
                    print "\t" + entityfilename + " has CommandPoints but no squads."
            elif 'pactUnlockEntityDefName' in line:
                entityname = line.replace('pactUnlockEntityDefName', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'UpgradeType ' in line and not 'linkedPlanetUpgradeType' in line:
                entityname = line.replace('UpgradeType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'cargoShipType ' in line:
                entityname = line.replace('cargoShipType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'Subject ' in line:
                entityname = line.strip().split()[1].replace('"', "")
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'afterColonizeBuffType ' in line:
                entityname = line.replace('afterColonizeBuffType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'flagship ' in line:
                entityname = line.strip().split()[1].replace('"', "")
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'entryVehicleType ' in line:
                entityname = line.replace('entryVehicleType', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'buffTypeToQuery ' in line:
                entityname = line.replace('buffTypeToQuery', "").replace('"', "").strip()
                if entityname != "" and not [entityname, filename] in entitylinked:
                    entitylinked.append([entityname, filename])
                    if not isModEntity(entityname + ".entity"):
                        notInMod(entityname, filename)
                        readFile(os.path.join(plaintextpath, entityname + ".entity"))
            elif 'meshName ' in line:
                meshname = line.strip().split()[1].replace('"', "").strip()
                if meshname != "" and not [meshname, filename] in meshlist:
                    meshlist.append([meshname, filename])
            elif 'MeshName' in line and ' "' in line:
                meshname = line.strip().split()[1].replace('"', "").strip()
                if meshname != "" and not [meshname, filename] in meshlist:
                    meshlist.append([meshname, filename])
            elif line.strip().startswith("picture "):
                brushname = line.replace("picture", "").replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif line.strip().startswith("backdrop "):
                brushname = line.replace("backdrop", "").replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif line.strip().startswith("underlay "):
                brushname = line.replace("underlay", "").replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif line.strip().startswith("overlay "):
                brushname = line.replace("overlay", "").replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif 'Backdrop' in line and ' "' in line:
                brushname = line.strip().split()[1].replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif ' "' in line and 'Overlay' in line.split()[0]:
                brushname = line.strip().split()[1].replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif 'Icon' in line and ' "' in line:
                brushname = line.strip().split()[1].replace('"', "").strip()
                if brushname != "" and not [brushname, filename] in brushlist:
                    brushlist.append([brushname, filename])
            elif line.strip().startswith("sound "):
                soundname = line.replace("sound", "").replace('"', "").strip()
                if soundname != "" and not [soundname, filename] in soundlist:
                    soundlist.append([soundname, filename])
            elif 'SoundID "' in line:
                soundname = line.strip().split()[1].replace('"', "")
                if soundname != "" and not [soundname, filename] in soundlist:
                    soundlist.append([soundname, filename])
            elif line.strip().startswith('musicTheme '):
                soundname = line.replace("musicTheme", "").replace('"', "").strip()
                if soundname != "" and not [soundname, filename] in soundlist:
                    soundlist.append([soundname, filename])
            elif line.strip().startswith('GameEventSound'):
                soundname = line.strip().split()[1].replace('"', "")
                if soundname != "" and not [soundname, filename] in soundlist:
                    soundlist.append([soundname, filename])
            if showcost and researchsubject and "Replicator_Research_Ability_Embargo.entity" not in filename:
                if 'pos [' in line:
                    researchpos = int(line.replace('pos [', "").strip()[0])
                if isinstance(researchpos, int):
                    if line.startswith('Tier '):
                        tier = int(line.replace("Tier", "").strip())
                        if researchpos != tier:
                            print "\tExpected Tier: " + str(researchpos) + " - Tier: " + str(tier) + " incorrect for " + filename
                    if line.startswith('BaseUpgradeTime'):
                        time = int(float(line.replace("BaseUpgradeTime", "").strip()))
                        totaltime = time
                        if researchtime[researchpos] != time:
                            print "\tExpected Time: " + str(researchtime[researchpos]) + " - Time: " + str(time) + " incorrect for " + filename
                    if line.startswith('PerLevelUpgradeTime '):
                        time = int(float(line.replace("PerLevelUpgradeTime", "").strip()))
                        if researchxtime[researchpos] != time:
                            print "\tExpected PerLevelTime: " + str(researchxtime[researchpos]) + " - PerLevelTime: " + str(time) + " incorrect for " + filename
                    if line.startswith('MaxNumResearchLevels'):
                        maxlevels = int(float(line.replace("MaxNumResearchLevels", "").strip()))
                    if line.startswith('PerLevelCostIncrease'):
                        costcomplete = True

                    if not costcomplete and 'credits ' in line:
                        cost = int(float(line.replace("credits", "").strip()))
                        totalcost = cost
                        if researchcredit[researchpos] != cost:
                            print "\tExpected Credits: " + str(researchcredit[researchpos]) + " - Credits: " + str(cost) + " incorrect for " + filename
                    elif 'credits ' in line:
                        cost = int(float(line.replace("credits", "").strip()))
                        if researchxcredit[researchpos] != cost:
                            print "\tExpected PerLevelCredits: " + str(researchxcredit[researchpos]) + " - PerLevelCredits: " + str(cost) + " incorrect for " + filename
                    if not costcomplete and 'metal ' in line:
                        cost = int(float(line.replace("metal", "").strip()))
                        if researchmetal[researchpos] != cost:
                            print "\tExpected Metal: " + str(researchmetal[researchpos]) + " - Metal: " + str(cost) + " incorrect for " + filename
                    elif 'metal ' in line:
                        cost = int(float(line.replace("metal", "").strip()))
                        if researchxmetal[researchpos] != cost:
                            print "\tExpected PerLevelMetal: " + str(researchxmetal[researchpos]) + " - PerLevelMetal: " + str(cost) + " incorrect for " + filename
                    if not costcomplete and 'crystal ' in line:
                        cost = int(float(line.replace("crystal", "").strip()))
                        if researchcrystal[researchpos] != cost:
                            print "\tExpected Crystal: " + str(researchcrystal[researchpos]) + " - Crystal: " + str(cost) + " incorrect for " + filename
                    elif 'crystal ' in line:
                        cost = int(float(line.replace("crystal", "").strip()))
                        if researchxcrystal[researchpos] != cost:
                            print "\tExpected PerLevelCrystal: " + str(
                            researchxcrystal[researchpos]) + " - PerLevelCrystal: " + str(cost) + " incorrect for " + filename

                if "Asuran" in os.path.basename(filename):
                    asurantime += totaltime * maxlevels / 60
                    asurancost += totalcost * maxlevels
                elif "Human" in os.path.basename(filename):
                    humantime += totaltime * maxlevels / 60
                    humancost += totalcost * maxlevels
                elif "Goauld" in os.path.basename(filename):
                    goauldtime += totaltime * maxlevels /60
                    goauldcost += totalcost * maxlevels

if basegame:
    if not excludebase:
        path = os.path.join(basegame, 'Textures')
        for filename in glob.glob(os.path.join(path, '*')):
            basegametextures.append(os.path.basename(filename).lower().replace(".tga", "").replace(".dds", ""))
        path = os.path.join(basegame, 'Particle')
        for filename in glob.glob(os.path.join(path, '*')):
            basegameparticles.append(os.path.basename(filename).lower().replace(".particle", ""))
        path = os.path.join(basegame, 'Sound')
        for filename in glob.glob(os.path.join(path, '*')):
            basegamesounds.append(os.path.basename(filename).lower())
    path = os.path.join(basegame, 'Mesh')
    for filename in glob.glob(os.path.join(path, '*')):
        basegamemeshes.append(os.path.basename(filename).lower().replace(".mesh", ""))
    path = os.path.join(basegame, 'GameInfo')
    for filename in glob.glob(os.path.join(path, '*')):
        basegameentites.append(os.path.basename(filename).lower())


print "** Reviewing Entity Manifest **"
i = 0
itemCount = 0
for line in open(os.path.join(rootpath, "entity.manifest")):
    if "entityNameCount" in line:
        itemCount = int(line.strip().split()[1])
    elif line.startswith("entityName"):
        i = i + 1
        entityval = line.replace("entityName", "").replace('"', "").strip()
        if not entityval in entitymanifest:
            entitymanifest.append(entityval)
        else:
            print "\tDuplicate entry in entity.manifest: " + entityval


if i != 0 and itemCount != i:
    print "\tentity.manifest"
    print "\t\tentityNameCount: " + str(itemCount) + ", entities: " + str(i)

print "** Reviewing Brush Counts **"
brushentries = []
path = os.path.join(rootpath, 'Window')
for filename in glob.glob(os.path.join(path, '*')):
    i = 0
    itemCount = 0
    linecount = 0
    for line in open(filename):
        if linecount == 0 and line.startswith("BIN"):
            binfiles.append(os.path.basename(filename))
            break
        linecount += 1
        if "brushCount" in line:
            itemCount = int(line.strip().split()[1])
        elif "brush\r\n" in line or "brush\n" in line:
            i = i + 1
        plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
        if 'fileName ' in line:
            brushfilename = line.replace('fileName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif 'textureName ' in line:
            brushfilename = line.replace('textureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif line.strip().startswith("name "):
            brushentry = line.replace('name ', "").replace('"', "").strip()
            if brushentry != "" and not [brushentry, filename] in brushentries:
                brushentries.append([brushentry, filename])
            elif [brushentry, filename] in brushentries:
                print "\tDuplicate Brush entry: " + brushentry + " in " + filename
        elif line.strip().startswith("leftPlayer ") or line.strip().startswith("rightPlayer "):
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif line.strip().startswith("sharedTech") and '"' in line:
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif line.strip().startswith("sharedCapitalShip") and '"' in line:
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif line.strip().startswith("leftFactionTech") and '"' in line:
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif line.strip().startswith("rightFactionTech") and '"' in line:
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))

    if i != 0 and itemCount != i:
        print "\t" + filename
        print "\t\tbrushCount: " + str(itemCount) + ", brushes: " + str(i)

path = os.path.join(rootpath, 'Galaxy')
for filename in glob.glob(os.path.join(path, '*')):
    linecount = 0
    for line in open(filename):
        if linecount == 0 and line.startswith("BIN"):
            binfiles.append(os.path.basename(filename))
            break
        linecount += 1
        if "browsePictureName " in line:
            brushfilename = line.replace('browsePictureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

print "** Reviewing Entity Values **"
researchtime = [40, 45, 50, 60, 75, 90, 105, 120]
researchxtime = [5, 5, 5, 5, 10, 10, 10, 10]
researchcredit = [400, 600, 800, 1000, 1200, 1400, 1600, 1800]
researchxcredit = [100, 100, 100, 100, 100, 100, 100, 100]
researchmetal = [0, 50, 100, 150, 200, 250, 300, 350]
researchxmetal = [0, 25, 25, 25, 25, 25, 25, 25]
researchcrystal = [25, 100, 175, 250, 325, 400, 475, 550]
researchxcrystal = [25, 25, 25, 25, 25, 25, 25, 25]
asurantime = 0
asurancost = 0
humantime = 0
humancost = 0
goauldtime = 0
goauldcost = 0
path = os.path.join(rootpath, 'GameInfo')

manualentry = ["AbilityWormHole", "BuffDecloakMineForMovement","BuffNeutralCapturableEntity","BuffRecentlyColonized",
    "PLANETMODULE_TECHORBITALCRYSTALEXTRACTOR", "PLANETMODULE_TECHORBITALMETALEXTRACTOR",
    "AbilityMinorFactionTradeCrystalForMetal", "AbilityMinorFactionTradeMetalForCrystal"]
for entityname in manualentry:
    if entityname != "" and not [entityname, "ManualEntry"] in entitylinked:
        entitylinked.append([entityname, "ManualEntry"])
        if not isModEntity(entityname + ".entity"):
            notInMod(entityname, "ManualEntry")
            readFile(os.path.join(plaintextpath, entityname + ".entity"))    

for filename in glob.glob(os.path.join(path, '*.entity')):
    readFile(filename)

if asurantime > 0:
    print "   ** Asuran Research Time: " + str(asurantime) + " minutes"
    print "   ** Asuran Research Credits: " + str(asurancost)
if humantime > 0:
    print "   ** Human Research Time: " + str(humantime) + " minutes"
    print "   ** Human Research Credits: " + str(humancost)
if goauldtime > 0:
    print "   ** Goauld Research Time: " + str(goauldtime) + " minutes"
    print "   ** Goauld Research Credits: " + str(goauldcost)

for filename in glob.glob(os.path.join(path, '*.randomeventdefs')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "spawnEntity " in line:
            entityname = line.replace('spawnEntity', "").replace('"', "").strip()
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif "excludedSpawnLocation " in line:
            entityname = line.replace('excludedSpawnLocation', "").replace('"', "").strip()
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif "buff " in line:
            entityname = line.replace('buff', "").replace('"', "").strip()
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))


for filename in glob.glob(os.path.join(path, '*.starscapedata')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if 'starsMesh ' in line:
            meshname = line.strip().split()[1].replace('"', "").strip()
            if meshname != "" and not [meshname, filename] in meshlist:
                meshlist.append([meshname, filename])

for filename in glob.glob(os.path.join(path, '*.musicdata')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "musicTheme" in line:
            soundname = line.replace('musicTheme', "").replace('"', "").strip()
            if soundname != "" and not [soundname, filename] in soundlinks:
                soundlinks.append([soundname, filename])

for filename in glob.glob(os.path.join(path, '*.coronadata')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "textureName" in line:
            brushfilename = line.replace('textureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

for filename in glob.glob(os.path.join(path, '*.lensflaredata')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "textureName" in line:
            brushfilename = line.replace('textureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

for filename in glob.glob(os.path.join(path, '*.starscapedata')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "starTextureName" in line:
            brushfilename = line.strip().split()[1].replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

for filename in glob.glob(os.path.join(path, '*.renderingDef')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "textureName " in line:
            brushfilename = line.replace('textureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

for filename in glob.glob(os.path.join(path, '*.constants')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    for line in open(filename):
        if "LevelUpEffectName " in line:
            particlename = line.replace('LevelUpEffectName', "").replace('"', "").strip()
            if particlename != "" and not [particlename, filename] in particlelist:
                particlelist.append([particlename, filename])
        elif "EffectName " in line:
            particlename = line.replace('EffectName', "").replace('"', "").strip()
            if particlename != "" and not [particlename, filename] in particlelist:
                particlelist.append([particlename, filename])
        elif "effectName " in line:
            particlename = line.replace('effectName', "").replace('"', "").strip()
            if particlename != "" and not [particlename, filename] in particlelist:
                particlelist.append([particlename, filename])
        elif 'type "' in line:
            entityname = line.replace('type', "").replace('"', "").strip()
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif 'QuestDefName ' in line:
            entityname = line.replace('QuestDefName', "").replace('"', "").strip()
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif 'ability:' in line:
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif 'FactionName' in line:
            stringname = line.replace('FactionName', "").replace('"', "").strip()
            if stringname != "" and not [stringname, filename] in stringlist:
                stringlist.append([stringname, filename])



for filename in glob.glob(os.path.join(path, '*.explosiondata')):
    for line in open(filename):
        if "particleSystemName " in line:
            particlename = line.replace('particleSystemName', "").replace('"', "").strip()
            if particlename != "" and not [particlename, filename] in particlelist:
                particlelist.append([particlename, filename])
        elif "sound " in line:
            soundname = line.replace("sound", "").replace('"', "").strip()
            if soundname != "" and not [soundname, filename] in soundlist:
                soundlist.append([soundname, filename])


print "** Reviewing Sound Counts **"
for filename in glob.glob(os.path.join(path, '*.sounddata')):
    i = 0
    itemCount = 0
    for line in open(filename):
        if "numEffects" in line or "numMusic" in line:
            itemCount = int(line.strip().split()[1])
        elif line.startswith("effect") or line.startswith("music"):
            i = i + 1
        elif line.strip().startswith("name "):
            soundname = line.replace('name', "").replace('"', "").strip()
            if soundname != "" and not [soundname, filename] in soundlinks:
                soundlinks.append([soundname, filename])
            elif [soundname, filename] in soundlinks:
                print "\tDuplicate Sound entry: " + soundname + " in " + filename
        elif line.strip().startswith("fileName "):
            soundfile = line.replace('fileName', "").replace('"', "").strip()
            if soundfile != "" and not [soundfile, filename] in soundfilelinks:
                soundfilelinks.append([soundfile, filename])
        
    if i != 0 and itemCount != i:
        print "\tIncorrect Count: " + filename
        print "\t\tNumEffects: " + str(itemCount) + ", Effect: " + str(i)

print "** Reviewing Skybox Counts **"
for filename in glob.glob(os.path.join(path, '*.skyboxbackdropdata')):
    i = 0
    itemCount = 0
    for line in open(filename):
        if "numProperties" in line:
            itemCount = int(line.strip().split()[1])
        elif line.startswith("properties"):
            i = i + 1
        elif "meshName " in line:
            meshname = line.replace('meshName', "").replace('"', "").strip()
            if meshname != "" and not [meshname, filename] in meshlist:
                meshlist.append([meshname, filename])
        elif "textureName " in line:
            brushfilename = line.replace('textureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "environmentMapName " in line:
            brushfilename = line.replace('environmentMapName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "environmentIlluminationMapName " in line:
            brushfilename = line.replace('environmentIlluminationMapName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

    if i != 0 and itemCount != i:
        print "\t" + filename
        print "\t\tnumProperties: " + str(itemCount) + ", Properties: " + str(i)

print "** Reviewing Asteroid Counts **"
for filename in glob.glob(os.path.join(path, '*.asteroidDef')):
    i = 0
    itemCount = 0
    for line in open(filename):
        if "meshGroupCount" in line:
            itemCount = int(line.strip().split()[1])
        elif line.startswith("meshGroup"):
            i = i + 1
        elif "meshName " in line:
            meshname = line.replace('meshName', "").replace('"', "").strip()
            if meshname != "" and not [meshname, filename] in  meshlist:
                meshlist.append([meshname, filename])

    if i != 0 and itemCount != i:
        print "\t" + filename
        print "\t\tmeshGroupCount: " + str(itemCount) + ", meshGroup: " + str(i)

print "** Reviewing Galaxy Scenario **"
for filename in glob.glob(os.path.join(path, '*.galaxyScenarioDef')):
    plaintextpath = os.path.join(os.path.expanduser(basegameplaintext),'GameInfo')
    starTypeCount = 0
    starType = 0
    planetTypeCount = 0
    planetType = 0
    orbitBodyTypeCount = 0
    orbitBodyType = 0
    planetItemTypeCount = 0
    planetItemType = 0
    playerTypeCount = 0
    playerType = 0
    planetItemsTemplateCount = 0
    planetItemsTemplate = 0
    validPictureGroups = 0
    pictureGroup = 0
    validThemeGroups = 0
    themeGroup = 0
    for line in open(filename):
        if "starTypeCount" in line:
            starTypeCount = int(line.strip().split()[1])
        elif line.startswith("starType"):
            starType = starType + 1
        elif "planetTypeCount" in line:
            planetTypeCount = int(line.strip().split()[1])
        elif line.startswith("planetType"):
            planetType = planetType + 1
        elif "orbitBodyTypeCount" in line:
            orbitBodyTypeCount = int(line.strip().split()[1])
        elif line.startswith("orbitBodyType"):
            orbitBodyType = orbitBodyType + 1
        elif "planetItemTypeCount" in line:
            planetItemTypeCount = int(line.strip().split()[1])
        elif line.startswith("planetItemType"):
            planetItemType = planetItemType + 1
        elif "playerTypeCount" in line:
            playerTypeCount = int(line.strip().split()[1])
        elif line.startswith("playerType"):
            playerType = playerType + 1
        elif "planetItemsTemplateCount" in line:
            planetItemsTemplateCount = int(line.strip().split()[1])
        elif line.startswith("planetItemsTemplate"):
            planetItemsTemplate = planetItemsTemplate + 1
        elif "validPictureGroups" in line:
            validPictureGroups = int(line.strip().split()[1])
        elif line.startswith("pictureGroup"):
            pictureGroup = pictureGroup + 1
        elif "validThemeGroups" in line:
            validThemeGroups = int(line.strip().split()[1])
        elif line.startswith("themeGroup"):
            themeGroup = themeGroup + 1
        elif 'entityDefName ' in line:
            entityname = line.replace('entityDefName', "").replace('"', "").strip()
            if entityname != "" and not [entityname, filename] in entitylinked:
                entitylinked.append([entityname, filename])
                if not isModEntity(entityname + ".entity"):
                    notInMod(entityname, filename)
                    readFile(os.path.join(plaintextpath, entityname + ".entity"))
        elif 'inGameName ' in line:
            stringname = line.replace('inGameName', "").replace('"', "").strip()
            if stringname != "" and not [stringname, filename] in stringlist:
                stringlist.append([stringname, filename])
        elif 'designStringId' in line:
            stringname = line.replace('designStringId', "").replace('"', "").strip()
            if stringname != "" and not [stringname, filename] in stringlist:
                stringlist.append([stringname, filename])

    if starType != 0 and starTypeCount != starType:
        print "\t\tGalaxyScenarioDef: (starTypeCount: " + str(starTypeCount) + ", starType: " + str(starType) + ")"
    if planetType != 0 and planetTypeCount != planetType:
        print "\t\tGalaxyScenarioDef: (planetTypeCount: " + str(planetTypeCount) + ", planetType: " + str(
            planetType) + ")"
    if orbitBodyType != 0 and orbitBodyTypeCount != orbitBodyType:
        print "\t\tGalaxyScenarioDef: (orbitBodyTypeCount: " + str(orbitBodyTypeCount) + ", orbitBodyType: " + str(
            orbitBodyType) + ")"
    if planetItemType != 0 and planetItemTypeCount != planetItemType:
        print "\t\tGalaxyScenarioDef: (planetItemTypeCount: " + str(planetItemTypeCount) + ", planetItemType: " + str(
            planetItemType) + ")"
    if playerType != 0 and playerTypeCount != playerType:
        print "\t\tGalaxyScenarioDef: (playerTypeCount: " + str(playerTypeCount) + ", playerType: " + str(
            playerType) + ")"
    if planetItemsTemplate != 0 and planetItemsTemplateCount != planetItemsTemplate:
        print "\t\tGalaxyScenarioDef: (planetItemsTemplateCount: " + str(
            planetItemsTemplateCount) + ", planetItemsTemplate: " + str(planetItemsTemplate) + ")"
    if pictureGroup != 0 and validPictureGroups != pictureGroup:
        print "\t\tGalaxyScenarioDef: (validPictureGroups: " + str(validPictureGroups) + ", pictureGroup: " + str(
            pictureGroup) + ")"
    if themeGroup != 0 and validThemeGroups != themeGroup:
        print "\t\tGalaxyScenarioDef: (validThemeGroups: " + str(validThemeGroups) + ", themeGroup: " + str(
            themeGroup) + ")"

for filename in glob.glob(os.path.join(path, '*')):
    if not filename.endswith(".entity"):
        #print "NonEntity: " + filename
        pass

path = os.path.join(rootpath, 'Particle')
for filename in glob.glob(os.path.join(path, '*')):
    particle = os.path.basename(os.path.splitext(filename)[0])
    particlefiles.append(particle)
    linecount = 0
    for line in open(filename):
        if linecount == 0 and line.startswith("BIN"):
            binfiles.append(os.path.basename(filename))
        linecount += 1
        if "textureName " in line:
            brushfilename = line.replace('textureName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "textureAnimationName " in line:
            brushfilename = line.replace('textureAnimationName', "").replace('"', "").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "MeshName " in line:
            meshfilename = line.replace('MeshName ', "").replace('"', "").strip()
            if meshfilename != "" and not [meshfilename, filename] in meshlist:
                meshlist.append([meshfilename, filename])

soundfiles = []
path = os.path.join(rootpath, 'Sound')
for filename in glob.glob(os.path.join(path, '*')):
    sound = os.path.basename(filename).lower()
    soundfiles.append(sound)

print "** Reviewing String Counts **"
path = os.path.join(rootpath, 'String')
stringids = []
for filename in glob.glob(os.path.join(path, '*')):
    i = 0
    itemCount = 0
    for line in open(filename):
        if "NumStrings" in line:
            itemCount = int(line.strip().split()[1])
        elif "StringInfo\r\n" in line or "StringInfo\n" in line:
            i = i + 1
        elif 'ID "' in line:
            stringval = line.replace('ID "', "").replace('"', "").strip()
            if not stringval.startswith("IDS_TAUNT") and stringval in stringids:
                print "\tDuplicate string in english.str: " + stringval
            stringids.append(stringval)
    if i != 0 and itemCount != i:
        print "\t" + filename
        print "\t\tNumStrings: " + str(itemCount) + ", StringInfo: " + str(i)

print "** Reviewing Mesh Counts **"
path = os.path.join(rootpath, 'Mesh')
meshnames = []
for filename in glob.glob(os.path.join(path, '*')):
    meshfile = os.path.basename(os.path.splitext(filename)[0])
    meshfiles.append(os.path.basename(filename))
    meshnames.append(meshfile)
    p = 0
    v = 0
    t = 0
    NumPoints = 0
    NumVertices = 0
    NumTriangles = 0
    linecount = 0
    for line in open(filename):
        if linecount == 0 and line.startswith("BIN"):
            binfiles.append(os.path.basename(filename))
        linecount += 1
        if "NumPoints" in line:
            NumPoints = int(line.strip().split()[1])
        elif "Point\r\n" in line or "Point\n" in line:
            p = p + 1
        elif "NumVertices" in line:
            NumVertices = int(line.strip().split()[1])
        elif "Vertex\r\n" in line or "Vertex\n" in line:
            v = v + 1
        elif "NumTriangles" in line:
            NumTriangles = int(line.strip().split()[1])
        elif "Triangle\r\n" in line or "Triangle\n" in line:
            t = t + 1
        elif "DataString" in line and "Flair-" in line:
            particlename = line.strip().split()[1].replace('"', "").replace('Flair-', "").strip()
            if particlename != "" and not [particlename, filename] in particlelist:
                particlelist.append([particlename, filename])
        elif "DiffuseTextureFileName " in line:
            brushfilename = line.replace('DiffuseTextureFileName', "").replace('"', "").strip()
            brushfilename = brushfilename.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "SelfIlluminationTextureFileName " in line:
            brushfilename = line.replace('SelfIlluminationTextureFileName', "").replace('"', "").strip()
            brushfilename = brushfilename.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "NormalTextureFileName " in line:
            brushfilename = line.replace('NormalTextureFileName', "").replace('"', "").strip()
            brushfilename = brushfilename.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "DisplacementTextureFileName " in line:
            brushfilename = line.replace('DisplacementTextureFileName', "").replace('"', "").strip()
            brushfilename = brushfilename.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])
        elif "TeamColorTextureFileName " in line:
            brushfilename = line.replace('TeamColorTextureFileName', "").replace('"', "").strip()
            brushfilename = brushfilename.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

    if p != 0 and NumPoints != p:
        print "\t" + filename
        print "\t\tNumPoints: " + str(NumPoints) + ", Points: " + str(p)
    if v != 0 and NumVertices != v:
        print "\t" + filename
        print "\t\tNumVertices: " + str(NumVertices) + ", Vertexs: " + str(v)
    if t != 0 and NumTriangles != t:
        print "\t" + filename
        print "\t\tNumTriangles: " + str(NumTriangles) + ", Triangles: " + str(t)

print "** Reviewing Squadrons **"
for filename in squadentities:
    squadcount = 0
    entityType = ""
    for line in open(filename):
        if "squadTypeEntityDef" in line:
            entityname = line.strip().split()[1].replace('"', "")
            if entityname != "":
                squadcount += 1
        elif 'entityType "' in line:
            entityType = line.replace('entityType', "").replace('"', "").strip()
    if entityType != "CapitalShip" and entityType != "Titan" and squadcount > 0:
        with open(filename, 'r+') as f:
            for line in f:
                if "baseCommandPoints" in line or "maxNumCommandPoints" in line:
                    commandpoints = float(line.strip().split()[1].replace('"', ""))
                    if commandpoints > squadcount and squadcount != 4:
                        entity = os.path.basename(filename)
                        print entity + " Frigate has " + str(commandpoints) + " Command Points but only " + str(squadcount) + " squads defined."
                    break
                elif "CommandPoints" in line:
                    line = f.next().strip()
                    commandpoints = float(line.strip().split()[1].replace('"', ""))
                    if commandpoints > squadcount and squadcount != 4:
                        entity = os.path.basename(filename)
                        print entity + " Frigate has " + str(commandpoints) + " Command Points but only " + str(squadcount) + " squads defined."
                    break

'''
print "** Reviewing Mesh **"
for listitem in meshlist:
    test = False
    for item in meshfiles:
        if listitem[0].lower().replace(".mesh", "") == item.lower().replace(".mesh", ""):
            test = True
            break
    if not test:
        print "\tMesh does not exist in Mesh Folder: " + listitem[0]
'''

print "** Reviewing Textures **"
path = os.path.join(rootpath, 'Textures')
textures = []
textures2 = []
for filename in glob.glob(os.path.join(path, '*')):
    texfile = os.path.basename(filename)
    if texfile in textures:
        print "\tDuplicate Texture (dds & tga): " + filename
    else:
        if not texfile in textures and not texfile in meshnames:
            textures.append(texfile)
    texfile = texfile.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").replace("-si.", ".").strip()
    if not texfile in textures2:
        textures2.append(texfile)

path = os.path.join(rootpath, 'TextureAnimations')
for filename in glob.glob(os.path.join(path, '*')):
    texfile = os.path.basename(filename)
    textures2.append(texfile)
    for line in open(filename):
        if "textureFileName" in line:
            brushfilename = line.replace('textureFileName', "").replace('"', "").strip()
            brushfilename = brushfilename.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip()
            if brushfilename != "" and not [brushfilename, filename] in texturelist:
                texturelist.append([brushfilename, filename])

entitymanlc = []
for entity in entitymanifest:
    entitymanlc.append(entity.lower())
for entity in entitylinked:
    if not str(entity[0] + ".entity").lower() in entitymanlc:
        print "\tEntity not referenced in the entity.manifest: " + entity[0]

if not verbose:
    print "** Reviewing File Formats **"
    if len(binfiles) > 0:
        print "\tUnable to read " + str(len(binfiles)) + " Binary Files"
else:
    print "\n***** Possible Unused Files ****\n"

    print "** Binary Files - Unable to read **"
    for item in binfiles:
        print "\tBinary File: " + item

    print "** Entities Not Referenced **"
    entitylist.sort()
    entitymanifest.sort()
    for entity in entitylist:
        if not entity in entitymanifest:
            print "\tEntity not referenced in the entity.manifest: " + entity

    print "** Particles Not Referenced **"
    for item in particlefiles:
        test = False
        for listitem in particlelist:
            if listitem[0].lower().replace(".particle", "") == item.lower().replace(".particle", ""):
                test = True
                break
        if not test:
            print "\tParticle not referenced by an Entity: " + item

    print "** Meshes Not Referenced **"
    for item in meshfiles:
        test = False
        for listitem in meshlist:
            if listitem[0].lower().replace(".mesh", "") == item.lower().replace(".mesh", ""):
                test = True
                break
        if not test:
            print "\tMeshes not referenced: " + item

    texturelist.sort(key=lambda x: x[0])

    print "** Textures Not Referenced **"
    for tex in textures2:
        #Base game defaults
        if tex.startswith("Cursor") or tex.startswith("LoadingSplash") or tex.startswith("Logo_Diplomacy"):
            continue
        #Extra but keep
        if tex == "BlackHole.dds" or tex == "pulsar_texture.dds" or tex == "sgi_logo.tga":
            continue
        ext = os.path.splitext(tex)
        test = False
        for file in texturelist:
            if file[0].lower().replace(".tga", "").replace(".dds", "") == tex.lower().replace(".tga", "").replace(".dds", ""):
                test = True
                break
        if not test:
            print "\tTexture not referenced in a plain text game file: " + tex
    
    print "** Bruses Not Referenced **"
    for brush in brushentries:
        test = False
        for item in brushlist:
            if item[0].lower() == brush[0].lower():
                test = True
                break
        if not test:
            #print "\tBrush not referenced in a plain text game file: " + brush[0]
            pass       

if buildman:
    print "\n** Write entity.manifest **"
    entitywrite = []
    for entity in entitylinked:
        if entity[0] + '.entity' not in entitywrite:
            entitywrite.append(entity[0] + '.entity')
    entitywrite.sort()
    file = open("entity.manifest", "w")
    file.write('TXT\n')
    file.write('entityNameCount ' + str(len(entitywrite)) + '\n')
    for entity in entitywrite:
        file.write('entityName "' + entity + '"\n')
    file.close()

print "\n***** Invalid Entries Check *****"

print "** Referenced Non-existant Entity **"
for entity in entitymanifest:
    test = False
    for listitem in entitylist:
        if listitem.lower() == entity.lower():
            test = True
            break
    if not test and not entity.lower() in basegameentites:
        print '\t"' + entity + '"' + ' listed in the entity.manifest does not appear to exist.'


print "** Referenced Non-existant Textures **"
for tex in texturelist:
    extension = os.path.splitext(tex[0])
    test = False
    dirstr = "Textures"
    tex[0] = tex[0].strip()
    if tex[0].endswith("texanim"):
        dirstr = "TextureAnimations"
    if len(extension[1]) > 0:
        for file in textures2:
            if file.lower() == tex[0].lower():
                test = True
                break
        if not test and not tex[0].lower().replace(".tga", "").replace(".dds", "") in basegametextures:
            for basetex in basegametextures:
                if basetex.replace("-cl.", ".").replace("-da.", ".").replace("-nm.", ".").replace("-bm.", ".").strip() == tex[0].lower().replace(".tga", "").replace(".dds", ""):
                    test = True
                    break
            if not test:
                print '\t"' + str(tex[0]) + '"' + ' listed in "' + str(tex[1]).replace(rootpath, "") + '" does not appear to exist in ' + dirstr + ' folder.'
    else:
        for file in textures2:
            file = os.path.splitext(file)[0]
            if file.lower() == tex[0].lower():
                test = True
                break
        if not test and not tex[0].lower().replace(".tga", "").replace(".dds", "") in basegametextures:
            print '\t"' + str(tex[0]) + '"' + ' listed in "' + str(tex[1]).replace(rootpath, "") + '" does not appear to exist in ' + dirstr + ' folder.'

print "** Referenced Non-existant String **"
for string in stringlist:
    test = False
    for itemlist in stringids:
        if string[0].lower() == itemlist.lower():
            test = True
            break
    if not test:
        print '\t"' + str(string[0]) + '"' + ' listed in "' + str(string[1]).replace(rootpath, "") + '" does not appear to exist in English.str.'

print "** Referenced Non-existant Mesh **"
for mesh in meshlist:
    meshval = mesh[0].lower().replace(".mesh", "")
    test = False
    for itemlist in meshfiles:
        if meshval == itemlist.lower().replace(".mesh", ""):
            test = True
            break
    if not test and not meshval in basegamemeshes:
        print '\t"' + str(mesh[0]) + '"' + ' listed in "' + str(mesh[1]).replace(rootpath, "") + '" does not appear to exist in Mesh folder.'


print "** Referenced Non-existant Sounddata **"
for sound in soundlist:
    test = False
    for itemlist in soundlinks:
        if sound[0] == itemlist[0]:
            test = True
            break
    if not test:
        print '\t"' + str(sound[0]) + '"' + ' listed in "' + str(sound[1]).replace(rootpath, "") + '" does not have a sounddata entry.'


print "** Referenced Non-existant Sound **"
for sound in soundfilelinks:
    test = False
    for itemlist in soundfiles:
        if sound[0].lower() == itemlist:
            test = True
            break
    if not test and not sound[0].lower() in basegamesounds:
        print '\t"' + str(sound[0]) + '"' + ' listed in "' + str(sound[1]).replace(rootpath, "") + '" does not appear to exist in Sound folder.'

print "** Referenced Non-existant Particle **"
for item in particlelist:
    test = False
    for itemlist in particlefiles:
        if item[0].lower() == itemlist.lower():
            test = True
            break
    if not test and not item[0].lower() in basegameparticles:
        print '\t"' + str(item[0]) + '"' + ' listed in "' + str(item[1]).replace(rootpath, "") + '" does not appear to exist in Particle folder.'

print "** Referenced Non-existant Brush **"
for item in brushlist:
    test = False
    for itemlist in brushentries:
        if item[0].lower() == itemlist[0].lower():
            test = True
            break
    if not test:
        print '\t"' + str(item[0]) + '"' + ' listed in "' + str(item[1]).replace(rootpath, "") + '" does not appear to exist in a Brush file.'


if verbose and basegame:
    print '\n*** Unnecessary File Check (Dups with Base) ***'
    if not skipbin:
        print '\tNote: this process may create a temporary file to properly compare a game binary.'
    baseDup('Textures')
    baseDup('Sound')
    baseDup('Mesh')
    baseDup('GameInfo')
    baseDup('Particle')
    baseDup('Galaxy')
    #baseDup('Window')


if graph:
    print '*** Writing Graph Files ***'
    file = open("graphedges.txt", "w")
    #file.write('From Type, From Name, Edge, To Type, To Name, Weight\n')
    for item in particlelist:
        file.write('Particle, ' + os.path.basename(
            os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(
            os.path.splitext(str(item[1]))[0]) + ', 1\n')
    for item in texturelist:
        if str(item[0]).endswith("texanim"):
            file.write('TextureAnimation, ' + os.path.basename(
                os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(
                os.path.splitext(str(item[1]))[0]) + ', 1\n')
        else:
            file.write('Texture, ' + os.path.basename(
                os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(
                os.path.splitext(str(item[1]))[0]) + ', 1\n')
    for item in meshlist:
        file.write(
            'Mesh, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(
                os.path.splitext(str(item[1]))[0]) + ', 1\n')
    #for item in entitylinked:
    #file.write('Entity, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(os.path.splitext(str(item[1]))[0]) + ', 1\n')
    file.close()
    file = open("graphnodes.txt", "w")
    #file.write('Type, Name\n')
    for item in particlefiles:
        file.write('Particle, ' + os.path.basename(os.path.splitext(str(item))[0]) + "\n")
    for item in textures2:
        if str(item).endswith("texanim"):
            file.write('TextureAnimation, ' + os.path.basename(os.path.splitext(str(item))[0]) + "\n")
        else:
            file.write('Texture, ' + os.path.basename(os.path.splitext(str(item))[0]) + "\n")
    for item in meshfiles:
        file.write('Mesh, ' + os.path.basename(os.path.splitext(str(item))[0]) + "\n")
    for item in entitylist:
        file.write('Entity, ' + os.path.basename(os.path.splitext(str(item))[0]) + "\n")
    file.close()

print '*** Completed ***'
