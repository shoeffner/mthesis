all: bio/BioID_0000.pgm

bio/BioID_%.pgm: BioID-FD-Eyepos-V1.2.zip BioID-FaceDatabase-V1.2.zip | bio
	@yes n | unzip -d bio BioID-FD-Eyepos-V1.2.zip 2> /dev/null
	@yes n | unzip -d bio BioID-FaceDatabase-V1.2.zip 2> /dev/null

BioID-FaceDatabase-V1.2.zip BioID-FD-Eyepos-V1.2.zip:
	curl -o $@ https://ftp.uni-erlangen.de/pub/facedb/$@

bio:
	@mkdir bio
