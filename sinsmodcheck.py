#The MIT License (MIT)
#Copyright (c) 2017 Stargate Invasion

import os
import glob
import sys
version = '1.1'

if len(sys.argv) > 1:
	rootpath = sys.argv[1]
else:
	print "\tUsage: simsmodcheck.py <moddirectory>"
	sys.exit()

print "\n***** Sins of Solar Empire Mod File Verifcation " + version + " *****"

texturelist = []
meshlist = []
stringlist = []
meshfilenamelist = []

print "** Reviewing Brush Counts **"
path =  os.path.join(rootpath, 'Window')
for filename in glob.glob(os.path.join(path, '*')):
	i = 0
	itemCount = 0
	for line in open(filename):
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
	for line in open(filename):
		if "browsePictureName " in line:
			brushfilename = line.replace('browsePictureName', "").replace('"', "").strip()
			if brushfilename != "" and not [brushfilename, filename] in texturelist:
	   			texturelist.append([brushfilename, filename])

path =  os.path.join(rootpath, 'GameInfo')
for filename in glob.glob(os.path.join(path, '*')):
	for line in open(filename):
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


path =  os.path.join(rootpath, 'Particle')
for filename in glob.glob(os.path.join(path, '*')):
	for line in open(filename):
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
	meshfilenamelist.append(os.path.basename(filename))
	meshnames.append(meshfile)
	p = 0
	v = 0
	t = 0
	NumPoints = 0
	NumVertices = 0
	NumTriangles = 0
	for line in open(filename):
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
			print '\t"' + str(tex[0]) + '"' + ' listed in "' + str(tex[1]) + '" does not appear to exist in ' + dirstr + '.'
	else:
		for file in textures2:
			file = os.path.splitext(file)[0]
			if file == tex[0]:
				test = True
				break
		if not test:
			print '\t"' + str(tex[0]) + '"' + ' listed in "' + str(tex[1]) + '" does not appear to exist in ' + dirstr + '.'

print "** Referenced Non-existant String **"
for string in stringlist:
	if not string[0] in stringids:
		print '\t"' + str(string[0]) + '"' + ' listed in "' + str(string[1]) + '" does not appear to exist in English.str.'


print "** Referenced Non-existant Mesh **"
for mesh in meshlist:
	if not mesh[0] in meshfilenamelist:
		print '\t"' + str(mesh[0]) + '"' + ' listed in "' + str(mesh[1]) + '" does not appear to exist in Mesh.'


   	