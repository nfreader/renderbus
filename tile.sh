#!/bin/bash

TILESIZE=256

for fullrender in *.png; do
	ZOOM=5
	mapname=${fullrender//'.png'/}
	mkdir -p "tiles/$mapname"
	MAPSIZE=`identify -format "%w" $fullrender`
	DESTDIR="tiles/$mapname"
	
	CROP="$TILESIZE"
	CROP+="x$TILESIZE"
	
	#Run the first tile pass on the main map size WITHOUT resizing
	mkdir -p $DESTDIR/tiles/$MAPNAME/$ZOOM
	convert $fullrender -crop $CROP +gravity -set filename:tile $DESTDIR/tiles/$MAPNAME/$ZOOM/tile_%[fx:page.x/$TILESIZE]-%[fx:page.y/$TILESIZE] %[filename:tile].png
	
	ZOOM=$[$ZOOM-1] #Since we're not resizing the first iteration, we skip a zoom level
	
	while [ $ZOOM -gt 0 ]
	do
	  MAPSIZE=$[$MAPSIZE/2]
	  RESIZE="$MAPSIZE"
	  RESIZE+="x$MAPSIZE"
	  mkdir -p $DESTDIR/tiles/$MAPNAME/$ZOOM
	  convert $fullrender -resize $RESIZE -crop $CROP +gravity -set filename:tile $DESTDIR/tiles/$MAPNAME/$ZOOM/tile_%[fx:page.x/$TILESIZE]-%[fx:page.y/$TILESIZE] %[filename:tile].png
	
	ZOOM=$[$ZOOM-1]
	done
done