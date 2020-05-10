#!/usr/bin/env python

"""
This is myphotobook-2-scribus.py. This script will create two Scribus documents
for a specific https://www.fotoalbum.es/
album created with their proprietary software (PhotoGenie X).

I guess it will work for albus created with aney of the other "country flavours"
of the franchise:
https://www.myphotobook.de/
https://www.myphotobook.at/
https://www.myphotobook.ch/
https://www.myphotobook.fr/
https://www.myphotobook.it/
https://www.myphotobook.nl
https://www.myphotobook.be
https://www.myphotobook.co.uk/
https://www.myphotobook.ie
https://www.myphotobook.se
https://www.myphotobook.dk

The directory where the album data are stored is in my case:
~users~\AppData\Roaming\PhotoGenie X\{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}\Persistent\Files\projects

The pictures used for the Albums are locally imported in the folder:
~users~\AppData\Roaming\PhotoGenie X\{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}\Persistent\Reserved
I renamed all the files in this folder with the .JPG extension, and that is how the scripts expects to find them. 
Is this is not the desired behaviour, then the next line has to be changed, from:
>> scribus.loadImage(imagedir + albumdata.pages[pagenum].layers[layercount].elements[elementcount].picture.id + ".JPG", f)
to
>> scribus.loadImage(imagedir + albumdata.pages[pagenum].layers[layercount].elements[elementcount].picture.id, f)

I haven't implemented any error checking in this version, as is is made for
my home purposes.

USAGE: It is probably better not to already have any document in Scribus,
since memory usage can become intense when a large number of images is
used.

You are first presented with a dialog to choose the .json album file, and then
the directory for the image files (usually /Persistent/Reserved/)

KNOWN ISSUES / NEED TO DEVELOP:
- Pictures across two pages are not presented properly, as they are doubled
  in both pages: Need to crop anything beyond the page limits
- Need to fix/implement image rotation, as we don't use them. There's an issue
  with some images with the attribute .contentRotation, even though the image
  be stright, the width and height attribute are interchanged.
- Sooo many things with fonts style and size and colour...
- Backgrounds are not taken into account

AUTHOR: Jesus Borruel Original version: 2018.01.30, this version: 2018.01.30

LICENSE: This program is free software; you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by the Free 
Software Foundation; either version 2 of the License, or (at your option) any 
later version.

text following the one presented in (scribalbum_letter.py)

"""

import scribus
import os
import json
import math

from HTMLParser import HTMLParser

#Global variable for keeping the caption text. Not the finest solution though...
caption_text = ""

class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		global caption_text
		#print "Data:", data
		caption_text = caption_text + data

# Read the JSON file into a PYTHON dictionary, which is easier to handle
class JSONObject:
	def __init__(self, d):
		self.__dict__ = d

jsonfile = scribus.fileDialog("Select Your JSON File", "*.JSON")
imagedir = scribus.fileDialog("Select Your Persistent - Reserved Directory", "Directories",isdir=True) + "/"
#jsonfile = "~users~/AppData/Roaming/PhotoGenie X/{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}/Persistent/Files/projects/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.json"
#imagedir = "~users~/AppData/Roaming/PhotoGenie X/{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}/Persistent/Reserved/"

# if the folder is copied somewhere else, as in temp, and want to run just one album file, for example:
#jsonfile = "C:/tmp/Fotoalbum/Persistent/Files/projects/891d2847-fd35-4bb9-a4c8-xxxxxxxxxxxx.json"
#imagedir = "C:/tmp/Fotoalbum/Persistent/Reserved/"

with open(jsonfile, 'r') as f:
	albumdata = json.load(f, object_hook=JSONObject)

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

pagenum = 0
layercount = 0
elementcount = 0

print "ALBUM datafile found:" + albumdata.descriptor.name

#In order to process only with a few pages, instead of the whole bunch of pages. Starting Page 1 is compulsory
#pages = [1,6,8]
#for pagenum in pages :

#In order to process only with the first few pages, instead of the whole bunch of pages. Starting Page 1 is compulsory
#for pagenum in range(1,16):

#To process only with the whole bunch of pages
for pagenum in range(len(albumdata.pages)):
	if pagenum == 0:
		# Cover page. Define font size for the Cover page captions, and new document style
		fontsize = 12
		size_x = albumdata.pages[pagenum].size.width
		size_y = albumdata.pages[pagenum].size.height
		# New doc with the cover pages
		scribus.newDoc((size_x,size_y), (3,3,3,3), scribus.PORTRAIT, 1, scribus.UNIT_MM, scribus.NOFACINGPAGES, scribus.FIRSTPAGERIGHT)
	elif pagenum == 1:
		# Album inner pages. Define font size for the album page's captions, and new document style
		fontsize = 8
		size_x = albumdata.pages[pagenum].size.width
		size_y = albumdata.pages[pagenum].size.height
		# New doc with the inner pages style
		scribus.newDoc((size_x,size_y), (3,3,3,3), scribus.PORTRAIT, 1, scribus.UNIT_MM, scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)  #libro para el resto de páginas
	else:
		# Insert new page within the album document
		scribus.newPage(-1)
	for layercount in range(len(albumdata.pages[pagenum].layers)):
		#print ("LAYER: " + str(layercount))
		if albumdata.pages[pagenum].layers[layercount].elements: #Check wether there are any elements within the layer, as it could be empty
			for elementcount in range(len(albumdata.pages[pagenum].layers[layercount].elements)):
				#print ("ELEMENT: " + str(elementcount))
				# I don't implement image rotation as we don't use it... Sorry
				# Check also if picture frame is empty, otherwise do not process it:
				if (albumdata.pages[pagenum].layers[layercount].elements[elementcount].type == 'PICTURE') and (albumdata.pages[pagenum].layers[layercount].elements[elementcount].picture != None) :
					size_x = albumdata.pages[pagenum].layers[layercount].elements[elementcount].size.width
					size_y = albumdata.pages[pagenum].layers[layercount].elements[elementcount].size.height
					x_pos = albumdata.pages[pagenum].layers[layercount].elements[elementcount].position.x - (size_x / 2)
					y_pos = albumdata.pages[pagenum].layers[layercount].elements[elementcount].position.y - (size_y / 2)	
					f = scribus.createImage(x_pos, y_pos, size_x, size_y)
					scribus.loadImage(imagedir + albumdata.pages[pagenum].layers[layercount].elements[elementcount].picture.id + ".JPG", f)
					scribus.setScaleImageToFrame(scaletoframe=1, proportional=0, name=f)
					# https://wiki.scribus.net/canvas/Fitting_an_Image_to_its_Frame
					# fitimage2frame_v2.py --> An advantage of this method is that will work regardless of the proportions of the image.
					# If you want to use this in Scribus versions >=1.5.0, you will need to change the scaleImage() command to setImageScale(), otherwise with the same parameters inside
					xscale, yscale = scribus.getImageScale(f)
					width_pi = int(albumdata.pages[pagenum].layers[layercount].elements[elementcount].picture.dimension.width) #original image width in pixels
					height_pi = int(albumdata.pages[pagenum].layers[layercount].elements[elementcount].picture.dimension.height) #original image height in pixels
					scribus.setScaleImageToFrame(scaletoframe=0, proportional=1, name=f)
					if (xscale > yscale):
						scale = xscale
						scribus.setImageScale(scale, scale, f)
						dpmm = width_pi/size_x # dots per mm of the current image
						offset_x = 0
						offset_y = -(height_pi/dpmm-size_y)/2/scribus.mm # scribus.mm --> scribus constant: millimetres in 1 pt
						if albumdata.pages[pagenum].layers[layercount].elements[elementcount].contentRotation > 0.1 : # I don't know why sometimes it mixes dimensions width and height
							offset_y = -(width_pi/dpmm-size_x)/2/scribus.mm # scribus.mm --> scribus constant: millimetres in 1 pt
					else:
						scale = yscale
						scribus.setImageScale(scale, scale, f)
						dpmm = height_pi/size_y # dots per mm of the current image
						offset_x = -(width_pi/dpmm-size_x)/2/scribus.mm # scribus.mm --> scribus constant: millimetres in 1 pt
						offset_y = 0
						if albumdata.pages[pagenum].layers[layercount].elements[elementcount].contentRotation > 0.1 :# I don't know why sometimes it mixes dimensions width and height
							offset_x = -(height_pi/dpmm-size_y)/2/scribus.mm # scribus.mm --> scribus constant: millimetres in 1 pt	
					scribus.setImageOffset(offset_x,offset_y, f) # offset comes in scribus units pts
					#If there is cropping, the image is "shifted" within the image frame, by a certain scale in points.
					if albumdata.pages[pagenum].layers[layercount].elements[elementcount].cropping:
						#Apply zoom and recenter
						zoom_x = float(albumdata.pages[pagenum].layers[layercount].elements[elementcount].cropping.width)
						zoom_y = float(albumdata.pages[pagenum].layers[layercount].elements[elementcount].cropping.height)
						if (zoom_x > zoom_y):
							scale = scale / zoom_x
							dpmm = dpmm * zoom_x
						elif (zoom_y > zoom_x):
							scale = scale / zoom_y
							dpmm = dpmm * zoom_y
						scribus.setImageScale(scale, scale, f)
						#Apply image shift within frame
						#Cropping is defined in myphotobook as the percentage of displacement from the centered picture, where 0.5 is centered, and extreme values (0,1)
						# is the maximum displacement and therefore to take out completely the image out of the frame
						x_shift = float(albumdata.pages[pagenum].layers[layercount].elements[elementcount].cropping.x) # % / 100 respect the center 0.5
						y_shift = float(albumdata.pages[pagenum].layers[layercount].elements[elementcount].cropping.y) # % / 100 respect the center 0.5
						offset_x = -(width_pi/dpmm-size_x)/2/scribus.mm+(0.5-x_shift)*width_pi/dpmm/scribus.mm # scribus.mm --> scribus constant: number of pts per mm
						offset_y = -(height_pi/dpmm-size_y)/2/scribus.mm+(0.5-y_shift)*height_pi/dpmm/scribus.mm
						scribus.setImageOffset(offset_x,offset_y, f)				
				elif (albumdata.pages[pagenum].layers[layercount].elements[elementcount].type == 'TEXT') and (albumdata.pages[pagenum].layers[layercount].elements[elementcount].text != ""):
					size_x = albumdata.pages[pagenum].layers[layercount].elements[elementcount].size.width
					size_y = albumdata.pages[pagenum].layers[layercount].elements[elementcount].size.height
					x_pos = albumdata.pages[pagenum].layers[layercount].elements[elementcount].position.x - (size_x / 2)
					y_pos = albumdata.pages[pagenum].layers[layercount].elements[elementcount].position.y - (size_y / 2)
					#This is the kind of text defined within the "text" label
					#<p style=\"text-align: left;\"><span style=\"color:#000000;font-family: Calibri; font-size: 2.82mm;\">Cataratas de Iguazú (Argentina) 27/11/2016</span></p>\n
					caption_text = ""
					parser.feed(albumdata.pages[pagenum].layers[layercount].elements[elementcount].text)
					#print "caption_text : " + caption_text
					captionBox = scribus.createText(x_pos,y_pos,size_x,size_y)
					scribus.setText(caption_text, captionBox)
					#scribus.setFont("Copper Std", captionBox)
					scribus.setFontSize(fontsize, captionBox)
					#The following are defined within the element attributes, but they don't seem to be used. The fonts are rather taken from the html info within the "text" attribute
					#scribus.setFont(albumdata.pages[pagenum].layers[layercount].elements[elementcount].font.family, captionBox)
					#scribus.setFontSize(albumdata.pages[pagenum].layers[layercount].elements[elementcount].font.size, captionBox)
					rotation = - albumdata.pages[pagenum].layers[layercount].elements[elementcount].rotation % (2 * math.pi)
					if rotation > 0.5 :
						# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
						# Scribus by default rotates the text box over the upper leftmost corner, while myphotobook uses the center point. 
						# Therefore, I use the function in the above site to translate the frame after rotation  
						# It works for most of our rotated text (upside down, as in the album spine) but sometimes not in the straight horizontal text
						#	ox, oy = origin
						ox, oy = 0,0
						#	px, py = point
						px, py = size_x/2, size_y/2
						qx = ox + math.cos(rotation) * (px - ox) - math.sin(rotation) * (py - oy)
						qy = oy + math.sin(rotation) * (px - ox) + math.cos(rotation) * (py - oy)
						scribus.rotateObjectAbs(math.degrees(rotation), captionBox)
						scribus.moveObject(size_x/2, size_y/2, captionBox)
						scribus.moveObject(qx, qy, captionBox)
						#print ("texto: " + str(caption_text))
						#print ("rotation: " + str(rotation))
						#print ("rotation degrees: " + str(math.degrees(rotation) % 360))
						#print ("----------------------------------------"+"\n")
				#else:
					#print ("no Elements within LAYER containing PICTURE or TEXT")
		#else:
			#print ("No elements within the LAYER")

scribus.setRedraw(1)
scribus.redrawAll()

