#The MIT License (MIT)
#Copyright (c) 2017 Stargate Invasion

import os
import glob
import sys
version = '1.2'
verbose = False
graph = False

if len(sys.argv) > 1:
	rootpath = sys.argv[1]
else:
	print "\tUsage: simsmodcheck.py <moddirectory> --showunused --graphexport"
	sys.exit()

if len(sys.argv) > 2:
	i = 2
	while i < len(sys.argv):
		if sys.argv[i] == "--showunused":
			verbose = True
		elif sys.argv[i] == "--graphexport":
			graph = True
		i += 1

print "\n***** Sins of Solar Empire Mod File Verifcation " + version + " *****"
if verbose:
	print "\nNote: Not all dependencies have been identified and Binary files in the mod are not read.  Files listed as UNUSED may be referenced by these binary files or not yet identified.\n"

texturelist = []
meshlist = []
stringlist = []
meshfiles = []
entitymanifest = []
entitylist = []
entitylinked = []
meshlinked = []
particlefiles = []
particlelist = []
binfiles = []

print "** Reviewing Entity Manifest **"
i = 0
itemCount = 0
for line in open(os.path.join(rootpath, "entity.manifest")):

	if "entityNameCount" in line:
   		itemCount = int(line.strip().split()[1])
   	elif line.startswith("entityName"):
   		i = i + 1
   		entitymanifest.append(line.replace("entityName", "").replace('"', "").strip())

if i !=0 and itemCount != i:
   	print "\tentity.manifest"
   	print "\t\tentityNameCount: " + str(itemCount) + ", entities: " + str(i)

print "** Reviewing Brush Counts **"
path =  os.path.join(rootpath, 'Window')
for filename in glob.glob(os.path.join(path, '*')):
	i = 0
	itemCount = 0
	linecount = 0
	for line in open(filename):
		if linecount == 0 and line.startswith("BIN"):
			binfiles.append(os.path.basename(filename))
		linecount += 1
		if "brushCount" in line:
   			itemCount = int(line.strip().split()[1])
   		elif "brush\r\n" in line or "brush\n" in line:
   			i = i + 1
   		if 'fileName ' in line:
   			brushfilename = line.replace('fileName', "").replace('"', "").strip()
   			if brushfilename != "" and not [brushfilename, filename] in texturelist:
   				texturelist.append([brushfilename, filename])
   		elif 'textureName ' in line:
   			brushfilename = line.replace('textureName', "").replace('"', "").strip()
   			if brushfilename != "" and not [brushfilename, filename] in texturelist:
   				texturelist.append([brushfilename, filename])

   	if i !=0 and itemCount != i:
   		print "\t" + filename
   		print "\t\tbrushCount: " + str(itemCount) + ", brushes: " + str(i)

path =  os.path.join(rootpath, 'Galaxy')
for filename in glob.glob(os.path.join(path, '*')):
	linecount = 0
	for line in open(filename):
		if linecount == 0 and line.startswith("BIN"):
			binfiles.append(os.path.basename(filename))
		linecount += 1
		if "browsePictureName " in line:
			brushfilename = line.replace('browsePictureName', "").replace('"', "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])

path =  os.path.join(rootpath, 'GameInfo')
for filename in glob.glob(os.path.join(path, '*.entity')):
	entitylist.append(os.path.basename(filename))
	linecount = 0
	for line in open(filename):
		if linecount == 0 and line.startswith("BIN"):
			binfiles.append(os.path.basename(filename))
		linecount += 1
		if "environmentMapName " in line:
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
	   	elif "textureName " in line:
			brushfilename = line.replace('textureName', "").replace('"', "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])
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
   		elif 'muzzleEffectName ' in line:
   			particlename = line.replace('muzzleEffectName', "").replace('"', "").strip()
   			if particlename != "" and not [particlename, filename] in particlelist:
   				particlelist.append([particlename, filename])
   		elif 'hitEffectName ' in line:
   			particlename = line.replace('hitEffectName', "").replace('"', "").strip()
   			if particlename != "" and not [particlename, filename] in particlelist:
   				particlelist.append([particlename, filename])
   		elif 'projectileTravelEffectName ' in line:
   			particlename = line.replace('projectileTravelEffectName', "").replace('"', "").strip()
   			if particlename != "" and not [particlename, filename] in particlelist:
   				particlelist.append([particlename, filename])
   		elif 'missileTravelEffectName ' in line:
   			particlename = line.replace('missileTravelEffectName', "").replace('"', "").strip()
   			if particlename != "" and not [particlename, filename] in particlelist:
   				particlelist.append([particlename, filename])
   		elif 'entityDefName ' in line:
   			entityname = line.replace('entityDefName', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'buffType ' in line:
   			entityname = line.replace('buffType', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'ability:0 ' in line:
   			entityname = line.replace('ability:0', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'ability:1 ' in line:
   			entityname = line.replace('ability:1', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'ability:2 ' in line:
   			entityname = line.replace('ability:2', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'ability:3 ' in line:
   			entityname = line.replace('ability:3', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'ability:4 ' in line:
   			entityname = line.replace('ability:4', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'squadTypeEntityDef:0 ' in line:
   			entityname = line.replace('squadTypeEntityDef:0', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'squadTypeEntityDef:1 ' in line:
   			entityname = line.replace('squadTypeEntityDef:1', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'squadTypeEntityDef:2 ' in line:
   			entityname = line.replace('squadTypeEntityDef:2', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'squadTypeEntityDef:3 ' in line:
   			entityname = line.replace('squadTypeEntityDef:3', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'UpgradeType ' in line:
   			entityname = line.replace('UpgradeType', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'cargoShipType ' in line:
   			entityname = line.replace('cargoShipType', "").replace('"', "").strip()
   			if entityname != "" and not [entityname, filename] in entitylinked:
   				entitylinked.append([entityname, filename])
   		elif 'randomMeshName ' in line:
   			meshname = line.replace('randomMeshName', "").replace('"', "").strip()
   			if meshname != "" and not [meshname, filename] in meshlinked:
   				meshlinked.append([meshname, filename])

path =  os.path.join(rootpath, 'Particle')
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
	   	if "textureAnimationName " in line:
			brushfilename = line.replace('textureAnimationName', "").replace('"', "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])
	   	if "MeshName " in line:
	   		meshfilename = line.replace('MeshName ', "").replace('"', "").strip()
			if meshfilename != "" and not [meshfilename, filename] in meshlist:
	   			meshlist.append([meshfilename, filename])

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
   			stringids.append(line.replace('ID "', "").replace('"', "").strip())
   	if i !=0 and itemCount != i:
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
   		elif "DiffuseTextureFileName " in line:
			brushfilename = line.replace('DiffuseTextureFileName', "").replace('"', "").strip()
			brushfilename = brushfilename.replace("-cl", "").replace("-da", "").replace("-nm", "").replace("-bm", "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])
	   	elif "SelfIlluminationTextureFileName " in line:
			brushfilename = line.replace('SelfIlluminationTextureFileName', "").replace('"', "").strip()
			brushfilename = brushfilename.replace("-cl", "").replace("-da", "").replace("-nm", "").replace("-bm", "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])
	   	elif "NormalTextureFileName " in line:
			brushfilename = line.replace('NormalTextureFileName', "").replace('"', "").strip()
			brushfilename = brushfilename.replace("-cl", "").replace("-da", "").replace("-nm", "").replace("-bm", "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])
	   	elif "DisplacementTextureFileName " in line:
			brushfilename = line.replace('DisplacementTextureFileName', "").replace('"', "").strip()
			brushfilename = brushfilename.replace("-cl", "").replace("-da", "").replace("-nm", "").replace("-bm", "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])
	   	elif "TeamColorTextureFileName " in line:
			brushfilename = line.replace('TeamColorTextureFileName', "").replace('"', "").strip()
			brushfilename = brushfilename.replace("-cl", "").replace("-da", "").replace("-nm", "").replace("-bm", "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])


   	if p !=0 and NumPoints != p:
   		print "\t" + filename
   		print "\t\tNumPoints: " + str(NumPoints) + ", Points: " + str(p)
   	if v !=0 and NumVertices != v:
   		print "\t" + filename
   		print "\t\tNumVertices: " + str(NumVertices) + ", Vertexs: " + str(v)
   	if t !=0 and NumTriangles != t:
   		print "\t" + filename
   		print "\t\tNumTriangles: " + str(NumTriangles) + ", Triangles: " + str(t)


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
	texfile = texfile.replace("-cl", "").replace("-da", "").replace("-nm", "").replace("-bm", "").replace("-si", "").strip()
	if not texfile in textures2:
		textures2.append(texfile)

path = os.path.join(rootpath, 'TextureAnimations')
for filename in glob.glob(os.path.join(path, '*')):
	texfile = os.path.basename(filename)
	textures2.append(texfile)

if verbose:
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
			if listitem[0] == item:
				test = True
				break
		if not test:
			print "\tEntity not referenced in the entity.manifest: " + item


	texturelist.sort(key=lambda x: x[0])

	print "** Textures Not Referenced **"
	for tex in textures2:
		ext = os.path.splitext(tex)
		test = False
		for file in texturelist:
			tmptext = tex
			ext2 = os.path.splitext(file[0])
			if len(ext[1]) > 0 and len(ext2[1]) == 0:
				tmptext = os.path.splitext(tex)[0]
			elif len(ext2[1]) > 0 and len(ext[1]) == 0:
				file[0] = os.path.splitext(file[0])[0]
			if file[0] == tmptext:
				test = True
				break
		if not test:
			print "\tTexture not referenced in a plain text game file: " + tex

print "\n***** Possible Bugs - Invalid Entries ****\n"

print "** Referenced Non-existant Entity **"
for entity in entitymanifest:
	if not entity in entitylist:
		print '\t"' + entity + '"' + ' listed in the entity.manifest does not appear to exist.'

print "** Referenced Non-existant Textures **"
for tex in texturelist:
	extension = os.path.splitext(tex[0])
	test = False
	dirstr = "Textures"
	if tex[0].endswith("texanim"):
		dirstr = "TextureAnimations"
	if len(extension[1]) > 0:
		for file in textures2:
			if file == tex[0]:
				test = True
				break
		if not test:
			print '\t"' + str(tex[0]) + '"' + ' listed in "' + str(tex[1]) + '" does not appear to exist in ' + dirstr + ' folder.'
	else:
		for file in textures2:
			file = os.path.splitext(file)[0]
			if file == tex[0]:
				test = True
				break
		if not test:
			print '\t"' + str(tex[0]) + '"' + ' listed in "' + str(tex[1]) + '" does not appear to exist in ' + dirstr + ' folder.'

print "** Referenced Non-existant String **"
for string in stringlist:
	if not string[0] in stringids:
		print '\t"' + str(string[0]) + '"' + ' listed in "' + str(string[1]) + '" does not appear to exist in English.str.'


print "** Referenced Non-existant Mesh **"
for mesh in meshlist:
	if not mesh[0] in meshfiles:
		print '\t"' + str(mesh[0]) + '"' + ' listed in "' + str(mesh[1]) + '" does not appear to exist in Mesh folder.'


print "** Referenced Non-existant Particle **"
for item in particlelist:
	if not item[0] in particlefiles:
		print '\t"' + str(item[0]) + '"' + ' listed in "' + str(item[1]) + '" does not appear to exist in Particle folder.'

if graph:
	print '*** Writing Graph Files ***'
	file = open("graphedges.txt","w") 
	#file.write('From Type, From Name, Edge, To Type, To Name, Weight\n')
	for item in particlelist:
		file.write('Particle, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(os.path.splitext(str(item[1]))[0]) + ', 1\n')
	for item in texturelist:
		if str(item[0]).endswith("texanim"):
			file.write('TextureAnimation, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(os.path.splitext(str(item[1]))[0]) + ', 1\n')
		else:
			file.write('Texture, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(os.path.splitext(str(item[1]))[0]) + ', 1\n')
	for item in meshlist:
		file.write('Mesh, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(os.path.splitext(str(item[1]))[0]) + ', 1\n')
	#for item in entitylinked:
		#file.write('Entity, ' + os.path.basename(os.path.splitext(str(item[0]))[0]) + ', Reference, Entity, ' + os.path.basename(os.path.splitext(str(item[1]))[0]) + ', 1\n')
	file.close()
	file = open("graphnodes.txt","w")
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


