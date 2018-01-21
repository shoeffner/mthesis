To run these files, remember to place the model files (shape predictor and
caffe models) inside the build directory.

To run bioid, you need to download the bioid files:
- https://ftp.uni-erlangen.de/pub/facedb/BioID-FaceDatabase-V1.2.zip
- https://ftp.uni-erlangen.de/pub/facedb/BioID-FD-Eyepos-V1.2.zip
end extract them into `bio` in [../../BioIDImages](../../BioIDImages).
However, the Makefile in that directory should take care of this.


The directory paths are otherwise relative to the build directory, so no
further action should be needed.
