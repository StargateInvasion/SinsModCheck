# SinsModCheck
A validation script for checking the consistency of a Sins of a Solar Empire Mod.

Checks for the following:
* Reviews Entity Manifest
* Reviews Brush Counts
* Reviews Entity Values
* Reviews Sound Counts
* Reviews Galaxy Scenario
* Reviews String Counts
* Reviews Mesh Counts
* Reviews Textures
* Referenced Non-existant Entity
* Referenced Non-existant Textures
* Referenced Non-existant String
* Referenced Non-existant Mesh
* Referenced Non-existant Sounddata
* Referenced Non-existant Sound
* Referenced Non-existant Particle
* Referenced Non-existant Brush

The script can also check for content that exists in the mod but doesn't appear to be in use - helping you clean up.  It will also compare the mod's files against the base game via md5, so that you can reduce duplication.
