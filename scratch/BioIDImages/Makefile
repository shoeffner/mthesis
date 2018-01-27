IMLIST = 0055 0115 0117 0121 0181 \
		 0238 0250 0275 0296 0345 \
		 0361 0444 0503 0581 0649 \
		 0660 0674 0941 0942 0967 \
		 0994 1016 1024 1029 1059 \
		 1092 1109 1121 1130 1142

IMAGE_DIR ?= $(abspath ../../assets/gen_files)

all: bio $(IMAGE_DIR)/BioID_exampleimages.png

$(IMAGE_DIR)/BioID_exampleimages.png: | bio Makefile
	montage $(foreach i,$(IMLIST),-label $(i) bio/BioID_$(i).pgm) \
		-tile x6 -geometry "120x120>+6+6" $@

bio: BioID-FD-Eyepos-V1.2.zip BioID-FaceDatabase-V1.2.zip
	@mkdir bio
	@yes n | unzip -d bio BioID-FD-Eyepos-V1.2.zip 2> /dev/null
	@yes n | unzip -d bio BioID-FaceDatabase-V1.2.zip 2> /dev/null

BioID-FaceDatabase-V1.2.zip BioID-FD-Eyepos-V1.2.zip:
	curl -o $@ https://ftp.uni-erlangen.de/pub/facedb/$@
