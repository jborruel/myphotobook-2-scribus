# myphotobook-2-scribus
This script will create two Scribus documents for a specific https://www.fotoalbum.es/ (or hopefully https://www.myphotobook.de/) album created with their proprietary software (PhotoGenie X)

I guess it will work for albums created with any of the other "country flavours"
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
