#!/usr/bin/env bash
#
# Plot Raypaths of SS and SS precursors
#

xmin=-25
xmax=$((xmin + 180))
gmt begin SS_raypath png
	gmt set FONT_TITLE 9p MAP_FRAME_PEN 1.25p MAP_TITLE_OFFSET 10p
	gmt basemap -JP8.0c+a+t65+fp -R${xmin}/${xmax}/0/6371 -B0

	# Plot upper mantle discontinuities, CMB, and ICB
	gmt basemap -Byg6371+410  -B+n --MAP_GRID_PEN_PRIMARY=0.5p,gray75
	gmt basemap -Byg6371+660  -B+n --MAP_GRID_PEN_PRIMARY=0.5p,gray75
	gmt basemap -Byg6371+2891 -B+n --MAP_GRID_PEN_PRIMARY=0.5p
	gmt basemap -Byg6371+5150 -B+n --MAP_GRID_PEN_PRIMARY=0.5p

	# Calculate raypath via TauP and plot
	taup_path -mod iasp91 -ph SS,S^410S -h 30 -deg 130 -o SS_raypath
	gmt plot SS_raypath.gmt -i0,1+s-1+o6371 -W0.5p,black
	rm SS_raypath.gmt
	echo 0   0 | gmt plot -Sa0.3c -Gred -N
	echo 130 0 | gmt plot -Si0.3c -Gblack -N

	# Add some label
	gmt text -F+f8p,Times-Roman+j -N -D0c/0.1c <<- EOF
	${xmax} 6371 BC Inner core
	${xmax} 4000 BC Outer core
	${xmax} 1800 BC Mantle
	EOF
	gmt text -F+f8p,Times-Roman+j -N <<- EOF
	70      220  MC SS
	65      1100 MC S@%6%d@%%S
	EOF

	gmt text -F+f8p,Times-Roman+j -D0c/0.12c -N <<- EOF
	65		0 BC bouncepoint
	0		0 BR source
	130		0 BL receiver
	EOF
gmt end show
